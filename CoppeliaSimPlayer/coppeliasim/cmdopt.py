def add(parser, mainPath):
    from pathlib import Path
    libPath = Path(mainPath).absolute().parent
    import platform
    plat = platform.system()
    if plat == 'Windows':
        libPath /= 'coppeliaSim.dll'
    elif plat == 'Linux':
        libPath /= 'libcoppeliaSim.so'
    elif plat == 'Darwin':
        libPath = libPath / '..' / 'MacOS' / 'libcoppeliaSim.dylib'
    parser.add_argument('-L', '--coppeliasim-library', metavar='library', type=str,
                        default=str(libPath),
                        help='Path to the coppeliaSim shared library')
    parser.add_argument('-c', '--startup-script-string', metavar='string', type=str,
                        help='Executes the script string as soon as the sandbox script is initialized')
    parser.add_argument('-v', '--verbosity', metavar='verbosity', type=str,
                        help='Sets the verbosity level, in the console. Default is loadinfos. Other accepted values are: none, errors, warnings, loadinfos, scripterrors, scriptwarnings, scriptinfos, infos, debug, trace, tracelua and traceall.')
    parser.add_argument('-w', '--statusbar-verbosity', metavar='verbosity', type=str,
                        help='Similar to -v, but for the verbosity level in the status bar. Default is scriptinfos.')
    parser.add_argument('-x', '--dlg-verbosity', metavar='verbosity', type=str,
                        help='Similar to -v, but for the verbosity level for simple dialogs. Default is infos. Other accepted values are: none, errors, warnings and questions.')
    parser.add_argument('-a', '--additional-addon-script-1', metavar='script', type=str,
                        help='Loads and runs an additional add-on specified via its filename.')
    parser.add_argument('-b', '--additional-addon-script-2', metavar='script', type=str,
                        help='Loads and runs an additional add-on specified via its filename.')
    parser.add_argument('-g', '--app-arg', metavar='arg', type=str,
                        action='append',
                        help='Represents an optional argument that can be queried within CoppeliaSim with the sim.stringparam_app_arg1 ... sim.stringparam_app_arg9 parameters.')
    parser.add_argument('-G', '--named-param', metavar='key=value', type=str,
                        action='append',
                        help='Set the named parameter, e.g. "key", to the given value.')
    parser.add_argument('-H', '--headless',
                        action='store_true',
                        help='Runs CoppeliaSim in headless mode (i.e. without any GUI).')
    parser.add_argument('-O', '--options', metavar='options', type=int, default=-1)

def parse(args):
    from ctypes import c_char_p
    from coppeliasim.lib import simSetStringParam, simSetNamedStringParam

    if args.startup_script_string:
        sim_stringparam_startupscriptstring = 125
        s = c_char_p(args.startup_script_string.encode('utf-8'))
        simSetStringParam(sim_stringparam_startupscriptstring, s)

    if args.verbosity:
        sim_stringparam_verbosity = 121
        s = c_char_p(args.verbosity.encode('utf-8'))
        simSetStringParam(sim_stringparam_verbosity, s)

    if args.statusbar_verbosity:
        sim_stringparam_statusbarverbosity = 122
        s = c_char_p(args.verbosity.encode('utf-8'))
        simSetStringParam(sim_stringparam_statusbarverbosity, s)

    if args.dlg_verbosity:
        sim_stringparam_dlgverbosity = 123
        s = c_char_p(args.verbosity.encode('utf-8'))
        simSetStringParam(sim_stringparam_dlgverbosity, s)

    if args.additional_addon_script_1:
        sim_stringparam_additional_addonscript1 = 11
        s = c_char_p(args.verbosity.encode('utf-8'))
        simSetStringParam(sim_stringparam_additional_addonscript1, s)

    if args.additional_addon_script_1:
        sim_stringparam_additional_addonscript2 = 12
        s = c_char_p(args.verbosity.encode('utf-8'))
        simSetStringParam(sim_stringparam_additional_addonscript2, s)

    if args.app_arg:
        for i, arg in enumerate(args.app_arg):
            sim_stringparam_app_arg1 = 2
            s = c_char_p(arg.encode('utf-8'))
            simSetStringParam(sim_stringparam_app_arg1 + i, s)

    if args.named_param:
        for i, arg in enumerate(args.named_param):
            k, v = arg.split('=', 1)
            k = c_char_p(k.encode('utf-8'))
            n = len(v)
            v = c_char_p(v.encode('utf-8'))
            simSetNamedStringParam(k, v, n)

    sim_gui_all = 0x0ffff
    sim_gui_headless = 0x10000
    if args.headless:
        options = sim_gui_headless
    else:
        options = sim_gui_all if args.options == -1 else args.options
    return options
