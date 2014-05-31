from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder, RootFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy('sosecreeet', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=RootFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/') #todo: login

    config.add_route('paste', '/paste') #paste form

    config.add_route('view', '/view/{id}') #See the resulting paste

    config.scan()

    return config.make_wsgi_app()
