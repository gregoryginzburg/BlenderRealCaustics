def alert(context, message, top_title):
    def draw(self, context):
        self.layout.label(text = message)
    context.window_manager.popup_menu(draw, title = top_title, icon = 'ERROR')
  