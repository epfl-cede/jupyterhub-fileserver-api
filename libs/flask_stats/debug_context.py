import sys


class debug_context:
    """Debug context to trace any function calls inside the context"""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("Entering Debug Decorated func")
        # Set the trace function to the trace_calls function
        # So all events are now traced
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        # Stop tracing all events
        sys.settrace = None

    def trace_calls(self, frame, event, arg):
        # We want to only trace our call to the decorated function
        if event != "call":
            return
        elif frame.f_code.co_name != self.name:
            return
        # return the trace function to use when you go into that
        # function call
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # If you want to print local variables each line
        # keep the check for the event 'line'
        # If you want to print local variables only on return
        # check only for the 'return' event
        if event not in ["line", "return"]:
            return
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        # filename = co.co_filename
        local_vars = frame.f_locals
        print("  {0} {1} {2} locals: {3}".format(func_name, event, line_no, local_vars))
