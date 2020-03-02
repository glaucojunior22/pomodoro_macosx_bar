import rumps

#rumps.debug_mode(True)


class PomodoroApp(object):
    def __init__(self):
        self.config = {
            'app_name': 'Pomodoro',
            'set_timer': 'Set Timer minutes',
            'start': 'Start Timer',
            'pause': 'Pause Timer',
            'continue': 'Continue Timer',
            'stop': 'Stop Timer',
            'break_message': 'Time is up! Take a break ;)',
            'interval': 25 * 60
        }
        self.app = rumps.App(self.config['app_name'])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval  = self.config['interval']
        self.set_up_menu()
        self.start_pause_button = rumps.MenuItem(
            title=self.config['set_timer'],
            callback=self.set_timer_minutes
        )
        self.stop_button = rumps.MenuItem(title=self.config['stop'],
                                          callback=None)
        self.app.menu = [self.start_pause_button, self.stop_button]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.icon = 'assets/icon.png'
        self.app.title = ''

    def set_timer_minutes(self, sender):
        window = rumps.Window(
            message='Enter the number of minutes for the timer',
            title='Timer Configuration',
            ok='Start Timer',
            cancel='Cancel',
            default_text='25',
            dimensions=(50, 20)
        )
        response = window.run()
        if response.clicked:
            try:
                minutes = int(response.text)
                self.interval = minutes * 60
                self.start_timer()
            except ValueError:
                rumps.notification(
                    title='Value Error',
                    subtitle='',
                    message='The value: {} is not a valid number.'.format(
                        response.text
                    )
                )

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            rumps.notification(title=self.config['app_name'],
                               subtitle=self.config['break_message'],
                               message='')
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

    def start_timer(self):
        self.start_pause_button.title = self.config['pause']
        self.start_pause_button.set_callback(self.pause_continue_timer)
        self.timer.count = 0
        self.timer.end = self.interval
        self.timer.start()

    def pause_continue_timer(self, sender):
        if sender.title == self.config['pause']:
            sender.title = self.config['continue']
            self.timer.stop()
        else:
            sender.title = self.config['pause']
            self.timer.start()

    def stop_timer(self, sender=None):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config['set_timer']
        self.start_pause_button.set_callback(self.set_timer_minutes)

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = PomodoroApp()
    app.run()