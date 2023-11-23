from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

# Write the code to be run here

profiler.stop()
profiler.print()