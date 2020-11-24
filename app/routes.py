from app import schedule_app as sapp


@sapp.route('/')
@sapp.route('/index')
def index():
    return 'Тут буде розклад'
