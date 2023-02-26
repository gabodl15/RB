from clients.models import Log
from clients.forms import ProfileForm
from routers.models import Router, Plan
from routers.functions import Connection
from logs.models import GlobalLog

class RouterProfile:
    
    def __init__(self, profile=None):
        if profile:
            self.profile = profile
            self.connection = Connection(self.profile.router)

    def conn(self, profile):
        self.connection = Connection(profile.router)
        return self.connection.active

    def create(self, request):
        form = ProfileForm(request.POST)
        _profile = form.save(commit=False)
        setattr(_profile, 'client_id', request.POST['client_id'])
        if self.conn(_profile):
            path = '/ppp/secret'
            context = {
                'name': request.POST['name'],
                'password': request.POST['password'],
                'plan': request.POST['plan'],
                'router': request.POST['router'],
                'connectio_mode': request.POST['connection_mode'],
            }
            self.connection.add(path, context)
            _profile.save()
            return True
        return False

    def update(self, request):
        new_name = request.POST['name']
        new_password = request.POST['password']
        new_mac = request.POST['mac']
        new_cutoff_date = request.POST['cutoff_date']
        new_router = Router.objects.get(id=request.POST['router'])
        new_plan = Plan.objects.get(id=request.POST['plan'])
        new_agreement = request.POST.get('agreement', False)

        get_user = self.connection.name_query('/ppp/secret', self.profile.name)

        if self.profile.name != new_name:
            self.connection.set_query('/ppp/secret', get_user[0]['id'], new_name)

        if self.profile.password != new_password:
            self.connection.set_query('/ppp/secret', get_user[0]['id'], 'password', new_password)
            self.profile.password = new_password

        if self.profile.mac != new_mac:
            self.profile.mac = new_mac

        # if self.profile.router != new_router:
        #     self.profile.router = new_router

        if self.profile.plan != new_plan:
            remove_from_active = self.connection.name_query('/ppp/active',self.profile.name)
            self.connection.set_query('/ppp/secret', get_user[0]['id'], 'profile', new_plan.name)
            if remove_from_active:
                self.connection.remove('/ppp/active', remove_from_active[0]['id'])

            self.profile.plan = new_plan


        if new_cutoff_date != '':
            self.profile.cutoff_date = new_cutoff_date

        if self.profile.agreement != new_agreement:
            self.profile.agreement = True if new_agreement == 'on' else False

        self.profile.save()

        self.connection.disconnect()

        global_log = GlobalLog(
            user=request.user,
            action='Edit PPP',
            message='PPP {} ha sido editado'.format(self.profile)
        )
        global_log.save()
        # message = 'Perfil actualizado'


        # return message
        return True

        def delete_ppp(self):
            secret_profile = self.connection.query_name('/ppp/secret', self.profile)
            if secret_profile:
                self.connection.remove('/ppp/secret', secret_profile[0]['id'])
            active_profile = self.connection.query_name('/ppp/secret', self.profile)
            if active_profile:
                self.connection.remove('/ppp/secret', active_profile[0]['id'])
                
            self.profile.remove()