# -*- coding: utf-8 -*-

import os
import hashlib
import uuid
import datetime

from flask import Flask, redirect, flash, request, current_app, url_for, abort, render_template, jsonify

from flask_admin import Admin, AdminIndexView as BaseAdminIndexView
from flask_admin.contrib.mongoengine import ModelView as BaseModelView
from flask_security import login_required, roles_required, roles_accepted
#from flask_security.decorators import http_auth_required, auth_token_required, auth_required
from flask_security import current_user

from models import Role, User, SocialConnection

_ = lambda s: s
gettext = lambda s: s

class RoledView(object):

    def _handle_view(self, name, *args, **kwargs):
        
        if not current_user.is_authenticated():
            abort(401)
        

class ModelView(RoledView, BaseModelView):
    pass

class AdminIndexView(RoledView, BaseAdminIndexView):
    pass
    
class RoleModelView(ModelView):
    _name = gettext(u"Rules")
    
    
class UserModelView(ModelView):
    _name = gettext(u"Users")
    
    #column_list = ('email', 'active', 'last_login_at', 'login_count')

class SocialConnectionModelView(ModelView):
    _name = gettext(u"Users")
    
def init_admin(app):

    admin = Admin(app, 
                  name=u"Flask-Social-Blueprint Admin",
                  index_view=AdminIndexView(), 
                  #base_template='layout.html', 
                  template_mode='bootstrap3')

    admin.add_view(RoleModelView(Role))
    admin.add_view(UserModelView(User))
    admin.add_view(SocialConnectionModelView(SocialConnection))
    
    
        
