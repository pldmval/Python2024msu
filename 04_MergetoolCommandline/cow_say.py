import cowsay
import cmd
import shlex

def complete_parametrs(text, line, begidx, endidx):
  args = shlex.split(line)
  args_len = len(args)
  eyes = ["OO", "XX", "==", "^^"]
  tongues = ["II", "VV", "UU", "JL"]
  if text == args[-1]:
    if args_len == 3:
      return [c for c in cowsay.list_cows() if c.startswith(text)]
    if args_len == 4:
      return [c for c in eyes if c.startswith(text)]
    if args_len == 5:
      return [c for c in tongues if c.startswith(text)]
  else:
    if args_len == 2:
      return [c for c in cowsay.list_cows() if c.startswith(text)]
    if args_len == 3:
      return [c for c in eyes if c.startswith(text)]
    if args_len == 4:
      return [c for c in tongues if c.startswith(text)]

def cowsay_and_cowthink(args):
  options = shlex.split(args)
  message = options[0]
  cow = 'default'
  eyes = 'OO'
  tongue = '  '
  for i in range(1, len(options)):
    if options[i] == "--cow":
      cow = options[i + 1]
    elif options[i] == "--eyes":
      eyes = options[i + 1]
    elif options[i] == "--tongue":
      tongue = options[i + 1]
  return [message, eyes, tongue, cow]

class CowSayCMD(cmd.Cmd):
  intro = "Welcome to the CowSay cmd."
  prompt = "moo >>>> "

  @staticmethod
  def do_list_cows(arg):
    """
		list_cows [dir]
		Lists all cow file names in the given directory or default cow list
		"""
    cowpath = None
    if arg:
      cowpath = shlex.split(arg)[0]
    print(*cowsay.list_cows(cowpath))

  @staticmethod
  def do_make_bubble(arg):
    """
		make_buble [wrap_text [width [brackets ]]]
		The text that appears above the cows
		"""
    options = shlex.split(arg)
    message = options[0]
    brackets = cowsay.THOUGHT_OPTIONS['cowsay']
    width = 40
    wrap_text = True
    for i in range(1, len(options)):
      if options[i] == "--wrap_text":
        wrap_text = bool(options[i + 1] == "true")
      elif options[i] == "--width":
        width = int(options[i + 1])
      elif options[i] == "--brackets":
        brackets = cowsay.THOUGHT_OPTIONS[options[i + 1]]
    print(cowsay.make_bubble(message, brackets=brackets, width=width, wrap_text=wrap_text))

  @staticmethod
  def complete_make_bubble(text, line, begidx, endidx):
    current_args = shlex.split(line)
    args_len = len(current_args)
    if ((args_len == 2 and current_args[-1] != text) or
            (args_len == 3 and current_args[-1] == text)):
      wrap_options = ['True', 'False']
      return [res for res in wrap_options if res.lower().startswith(text.lower())]

  @staticmethod
  def do_cowsay(arg):
    """
		cowsay message [cow [eyes [tongue]]]
		Display a message as cow phrase
		"""
    message, eyes, tongue, cow = cowsay_and_cowthink(arg)
    print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))

  @staticmethod
  def do_cowthink(arg):
    """
		cowthink message [cow [eyes [tongue]]]
		Display a message as cow thought
		"""
    message, eyes, tongue, cow = cowsay_and_cowthink(arg)
    print(cowsay.cowthink(message, eyes=eyes, tongue=tongue, cow=cow))

  @staticmethod
  def complete_cowsay(text, line, begidx, endidx):
    return complete_parametrs(text, line, begidx, endidx)
  @staticmethod
  def complete_cowthink(text, line, begidx, endidx):
    return complete_parametrs(text, line, begidx, endidx)

  @staticmethod
  def do_exit(arg):
    """
    Exit cow command line
    """
    return True

if __name__ == '__main__':
  CowSayCMD().cmdloop()
