from pyramid.view import view_config
import deform
import colander
from pyramid.response import Response
import pyramid.httpexceptions as exc

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .security import USERS, PASS

from crypt import crypt

def render_form(request,form, appstruct=colander.null, submitted='submit', success=None, readonly=False):
    captured = None

    if submitted in request.POST:
        # the request represents a form submission
        try:
            # try to validate the submitted values
            controls = request.POST.items()
            captured = form.validate(controls)
            if success:
                response = success(captured['text'],captured['lang'])
                if response is not None:
                    return response
            html = form.render(captured)
        except deform.ValidationFailure as e:
            # the submitted values could not be validated
            html = e.render()

    else:
        # the request requires a simple form rendering
        html = form.render(appstruct, readonly=readonly)

    if request.is_xhr:
        return Response(html)

    # values passed to template for rendering
    return {
        'form':html
        }

@view_config(route_name='home', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def my_view(request):
    login_url = request.route_url('home')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.POST:
        login = request.POST['login']
        password = request.POST['password']
        if crypt(password,PASS.get(login))==PASS.get(login):
            headers = remember(request, login)
            return exc.HTTPFound(location = '/paste',
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/',
        came_from = came_from,
        login = login,
        password = password,
        )


@view_config(route_name='paste', renderer='templates/paste.jinja2', permission='edit')
def paste(request):
    choices = (
        ('abap','ABAP'),
        ('ada','Ada'),
        ('ahk','autohotkey'),
        ('antlr','ANTLR'),
        ('antlr-as','ANTLR With ActionScript Target'),
        ('antlr-cpp','ANTLR With CPP Target'),
        ('antlr-csharp','ANTLR With C# Target'),
        ('antlr-java','ANTLR With Java Target'),
        ('antlr-objc','ANTLR With ObjectiveC Target'),
        ('antlr-perl','ANTLR With Perl Target'),
        ('antlr-python','ANTLR With Python Target'),
        ('antlr-ruby','ANTLR With Ruby Target'),
        ('apacheconf','ApacheConf'),
        ('applescript','AppleScript'),
        ('as','ActionScript'),
        ('as3','ActionScript 3'),
        ('aspectj','AspectJ'),
        ('aspx-cs','aspx-cs'),
        ('aspx-vb','aspx-vb'),
        ('asy','Asymptote'),
        ('autoit','AutoIt'),
        ('awk','Awk'),
        ('basemake','Base Makefile'),
        ('bash','Bash'),
        ('bat','Batchfile'),
        ('bbcode','BBCode'),
        ('befunge','Befunge'),
        ('blitzmax','BlitzMax'),
        ('boo','Boo'),
        ('brainfuck','Brainfuck'),
        ('bro','Bro'),
        ('bugs','BUGS'),
        ('c','C'),
        ('ca65','ca65'),
        ('cbmbas','CBM BASIC V2'),
        ('ceylon','Ceylon'),
        ('cfengine3','CFEngine3'),
        ('cfm','Coldfusion HTML'),
        ('cfs','cfstatement'),
        ('cheetah','Cheetah'),
        ('Clipper','FoxPro'),
        ('clojure','Clojure'),
        ('cmake','CMake'),
        ('c-objdump','c-objdump'),
        ('cobol','COBOL'),
        ('cobolfree','COBOLFree'),
        ('coffee-script','CoffeeScript'),
        ('common-lisp','Common Lisp'),
        ('console','Bash Session'),
        ('control','Debian Control file'),
        ('coq','Coq'),
        ('cpp','C++'),
        ('cpp-objdump','cpp-objdump'),
        ('croc','Croc'),
        ('csharp','C#'),
        ('css','CSS'),
        ('css+django','CSS+Django/Jinja'),
        ('css+erb','CSS+Ruby'),
        ('css+genshitext','CSS+Genshi Text'),
        ('css+lasso','CSS+Lasso'),
        ('css+mako','CSS+Mako'),
        ('css+myghty','CSS+Myghty'),
        ('css+php','CSS+PHP'),
        ('css+smarty','CSS+Smarty'),
        ('Cucumber','Gherkin'),
        ('cuda','CUDA'),
        ('cython','Cython'),
        ('d','D'),
        ('dart','Dart'),
        ('delphi','Delphi'),
        ('dg','dg'),
        ('diff','Diff'),
        ('django','Django/Jinja'),
        ('d-objdump','d-objdump'),
        ('dpatch','Darcs Patch'),
        ('dtd','DTD'),
        ('duel','Duel'),
        ('dylan','Dylan'),
        ('dylan-console','Dylan session'),
        ('dylan-lid','DylanLID'),
        ('ec','eC'),
        ('ecl','ECL'),
        ('elixir','Elixir'),
        ('erb','ERB'),
        ('erl','Erlang erl session'),
        ('erlang','Erlang'),
        ('evoque','Evoque'),
        ('factor','Factor'),
        ('fan','Fantom'),
        ('fancy','Fancy'),
        ('felix','Felix'),
        ('fortran','Fortran'),
        ('fsharp','FSharp'),
        ('gas','GAS'),
        ('genshi','Genshi'),
        ('genshitext','Genshi Text'),
        ('glsl','GLSL'),
        ('gnuplot','Gnuplot'),
        ('go','Go'),
        ('gooddata-cl','GoodData-CL'),
        ('gosu','Gosu'),
        ('groff','Groff'),
        ('groovy','Groovy'),
        ('gst','Gosu Template'),
        ('haml','Haml'),
        ('haskell','Haskell'),
        ('haxeml','Hxml'),
        ('html','HTML'),
        ('html+cheetah','HTML+Cheetah'),
        ('html+django','HTML+Django/Jinja'),
        ('html+evoque','HTML+Evoque'),
        ('html+genshi','HTML+Genshi'),
        ('html+lasso','HTML+Lasso'),
        ('html+mako','HTML+Mako'),
        ('html+myghty','HTML+Myghty'),
        ('html+php','HTML+PHP'),
        ('html+smarty','HTML+Smarty'),
        ('html+velocity','HTML+Velocity'),
        ('http','HTTP'),
        ('hx','haXe'),
        ('hybris','Hybris'),
        ('idl','IDL'),
        ('iex','Elixir iex session'),
        ('ini','INI'),
        ('io','Io'),
        ('ioke','Ioke'),
        ('irc','IRC logs'),
        ('jade','Jade'),
        ('jags','JAGS'),
        ('java','Java'),
        ('jlcon','Julia console'),
        ('js','JavaScript'),
        ('js+cheetah','JavaScript+Cheetah'),
        ('js+django','JavaScript+Django/Jinja'),
        ('js+erb','JavaScript+Ruby'),
        ('js+genshitext','JavaScript+Genshi Text'),
        ('js+lasso','JavaScript+Lasso'),
        ('js+mako','JavaScript+Mako'),
        ('js+myghty','JavaScript+Myghty'),
        ('js+php','JavaScript+PHP'),
        ('js+smarty','JavaScript+Smarty'),
        ('json','JSON'),
        ('jsp','Java Server Page'),
        ('julia','Julia'),
        ('kconfig','Kconfig'),
        ('koka','Koka'),
        ('kotlin','Kotlin'),
        ('lasso','Lasso'),
        ('lhs','Literate Haskell'),
        ('lighty','Lighttpd configuration file'),
        ('live-script','LiveScript'),
        ('llvm','LLVM'),
        ('logos','Logos'),
        ('logtalk','Logtalk'),
        ('lua','Lua'),
        ('make','Makefile'),
        ('mako','Mako'),
        ('maql','MAQL'),
        ('mason','Mason'),
        ('matlab','Matlab'),
        ('matlabsession','Matlab session'),
        ('minid','MiniD'),
        ('modelica','Modelica'),
        ('modula2','Modula-2'),
        ('monkey','Monkey'),
        ('moocode','MOOCode'),
        ('moon','MoonScript'),
        ('mscgen','Mscgen'),
        ('mupad','MuPAD'),
        ('mxml','MXML'),
        ('myghty','Myghty'),
        ('mysql','MySQL'),
        ('nasm','NASM'),
        ('nemerle','Nemerle'),
        ('newlisp','NewLisp'),
        ('newspeak','Newspeak'),
        ('nginx','Nginx configuration file'),
        ('nimrod','Nimrod'),
        ('nsis','NSIS'),
        ('numpy','NumPy'),
        ('objdump','objdump'),
        ('objective-c','Objective-C'),
        ('objective-c++','Objective-C++'),
        ('objective-j','Objective-J'),
        ('ocaml','OCaml'),
        ('octave','Octave'),
        ('ooc','Ooc'),
        ('opa','Opa'),
        ('openedge','OpenEdge ABL'),
        ('perl','Perl'),
        ('php','PHP'),
        ('plpgsql','PL/pgSQL'),
        ('postgresql','PostgreSQL SQL dialect'),
        ('postscript','PostScript'),
        ('pot','Gettext Catalog'),
        ('pov','POVRay'),
        ('powershell','PowerShell'),
        ('prolog','Prolog'),
        ('properties','Properties'),
        ('protobuf','Protocol Buffer'),
        ('psql','PostgreSQL console (psql)'),
        ('puppet','Puppet'),
        ('py3tb','Python 3.0 Traceback'),
        ('pycon','Python console session'),
        ('pypylog','PyPy Log'),
        ('pytb','Python Traceback'),
        ('python','Python'),
        ('python3','Python 3'),
        ('qml','QML'),
        ('racket','Racket'),
        ('ragel','Ragel'),
        ('ragel-c','Ragel in C Host'),
        ('ragel-cpp','Ragel in CPP Host'),
        ('ragel-d','Ragel in D Host'),
        ('ragel-em','Embedded Ragel'),
        ('ragel-java','Ragel in Java Host'),
        ('ragel-objc','Ragel in Objective C Host'),
        ('ragel-ruby','Ragel in Ruby Host'),
        ('raw','Raw token data'),
        ('rb','Ruby'),
        ('rbcon','Ruby irb session'),
        ('rconsole','RConsole'),
        ('rd','Rd'),
        ('rebol','REBOL'),
        ('redcode','Redcode'),
        ('registry','reg'),
        ('rhtml','RHTML'),
        ('RobotFramework','RobotFramework'),
        ('rst','reStructuredText'),
        ('rust','Rust'),
        ('sass','Sass'),
        ('scala','Scala'),
        ('scaml','Scaml'),
        ('scheme','Scheme'),
        ('scilab','Scilab'),
        ('scss','SCSS'),
        ('shell-session','Shell Session'),
        ('smali','Smali'),
        ('smalltalk','Smalltalk'),
        ('smarty','Smarty'),
        ('sml','Standard ML'),
        ('snobol','Snobol'),
        ('sourceslist','Debian Sourcelist'),
        ('sp','SourcePawn'),
        ('spec','RPMSpec'),
        ('splus','S'),
        ('sql','SQL'),
        ('sqlite3','sqlite3con'),
        ('squidconf','SquidConf'),
        ('ssp','Scalate Server Page'),
        ('stan','Stan'),
        ('systemverilog','systemverilog'),
        ('tcl','Tcl'),
        ('tcsh','Tcsh'),
        ('tea','Tea'),
        ('tex','TeX'),
        ('text','Text only'),
        ('trac-wiki','MoinMoin/Trac Wiki markup'),
        ('treetop','Treetop'),
        ('ts','TypeScript'),
        ('urbiscript','UrbiScript'),
        ('vala','Vala'),
        ('vb.net','VB.net'),
        ('velocity','Velocity'),
        ('verilog','verilog'),
        ('vgl','VGL'),
        ('vhdl','vhdl'),
        ('vim','VimL'),
        ('xml','XML'),
        ('xml+cheetah','XML+Cheetah'),
        ('xml+django','XML+Django/Jinja'),
        ('xml+erb','XML+Ruby'),
        ('xml+evoque','XML+Evoque'),
        ('xml+lasso','XML+Lasso'),
        ('xml+mako','XML+Mako'),
        ('xml+myghty','XML+Myghty'),
        ('xml+php','XML+PHP'),
        ('xml+smarty','XML+Smarty'),
        ('xml+velocity','XML+Velocity'),
        ('xquery','XQuery'),
        ('xslt','XSLT'),
        ('xtend','Xtend'),
        ('yaml','YAML'),
            )
    class Schema(colander.Schema):
        lang = colander.SchemaNode(
                colander.String(),
                title='Language',
                widget=deform.widget.SelectWidget(values=choices),
                default='python'
                )
        text = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(max=10000),
                widget=deform.widget.TextAreaWidget(rows=20, cols=85),
                description='Enter some text')
    schema = Schema()
    options = """
    {success:
      function (rText, sText, xhr, form) {
        var loc = xhr.getResponseHeader('X-Relocate');
        if (loc) {
          document.location = loc;
        };
       }
    }
    """
    def succeed(text,lang):
        id = make_paste(text,lang)
        location = '/view/' + id
        # To appease jquery 1.6+, we need to return something that smells
        # like HTML, or we get a "Node cannot be inserted at the
        # specified point in the hierarchy" Javascript error.  This didn't
        # used to be required under JQuery 1.4.
        #return Response(
        #    '<div>Please wait</div>',
        #    headers=[('X-Relocate', location), ('Content-Type','text/html')]
        #    )
        raise exc.HTTPFound(location)
    form = deform.Form(schema, buttons=('submit',), use_ajax=True,
                           ajax_options=options)
    return render_form(request,form, success=succeed)

@view_config(route_name='view', renderer='templates/view.jinja2')
def view(request):
    id = request.matchdict.get('id', -1)
    if os.path.exists('simplewebpaste/pastes/%s' % id):
        with open('simplewebpaste/pastes/%s' % id, 'rb') as f:
            html = f.read()
            f.close()
    else:
        html = ''
    return({'html':html})

import tempfile
import pygments
#Python 2 doesn't like this??
#import pygments.lexers as p_lexers
from pygments.lexers import get_lexer_by_name
import pygments.formatters as p_formatters
import pygments.styles as p_styles
import irc_highlight
import base64
import datetime
import os
import os.path
import sys

STYLE = 'monokai'


def generate_token():
    now = datetime.datetime.now()
    stamp = now.strftime('%y%m%d.%H%M%S.')
    key = base64.b32encode(open('/dev/urandom', 'rb').read(5)).decode('latin-1').lower()
    return stamp+key

def upload(data, destpath):
    with open('simplewebpaste/pastes/%s' % destpath, 'wb') as f:
        f.write(data)

def format_text(config, text):
    if config['in_lang'] == 'irc':
        return irc_highlight.highlight(text)
    else:
        lexer = get_lexer_by_name(config['in_lang'])
        style = p_styles.get_style_by_name(STYLE)
        formatter = p_formatters.HtmlFormatter(linenos=config['linenos'], cssclass='pb', style=style)
        html = pygments.highlight(text, lexer, formatter)
        return html

def make_paste(data,lang):
    configuration = {
        'in_lang': lang,
        'linenos': 'table',
    }
    
    result = format_text(configuration, data)
    output = u'''<!DOCTYPE html><html><head>
    <!--
        Configuration:
        {config}
        -->
    <link rel='stylesheet' href='/static/style.css' type='text/css'>
    </head><body>
    {text}
    </body></html>'''.format(
        config=repr(configuration),
        text=result)

    token = generate_token()
    upload(output.encode('utf-8'), token)
    upload(data.encode('utf-8'), 'raw/%s' % token)
    return(token)
