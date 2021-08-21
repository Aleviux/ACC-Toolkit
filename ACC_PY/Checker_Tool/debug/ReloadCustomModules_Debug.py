def reloadCustomModules(userPath=None):
    """
    Reloads all custom modules for the current session.
    It's going to have a flag to let you specify the userPath you want to clear out,
    but otherwise it's going to assume that it's the parent dir of the folder the script is in.
    @memberOf: -
    @params: userPath (string)
    @returns: -
    @example-use:
        reloadCustomModules()
    """

    import inspect, sys, os
    from os.path import dirname

    if userPath is None:
        currentPath = os.path.dirname(os.path.abspath(__file__))
        parentPath = os.path.abspath(os.path.join(currentPath, os.pardir))
        userPath = parentPath

    # Convert this to lower just for a clean comparison later
    userPath = userPath.lower()

    toDelete = []

    # Iterate over all the modules that are currently loaded
    for key, module in sys.modules.items():

        # There's a few modules that are going to complain if you try to query them
        # so I've popped this into a try/except to keep it safe
        try:

            # Use the "inspect" library to get the moduleFilePath that the current module was loaded from
            moduleFilePath = inspect.getfile(module).lower()

            # Don't try and remove the startup script, that will break everything
            if moduleFilePath == __file__.lower():
                continue

            # Don't delete the __main__ module
            if key == "__main__":
                continue

            # If the module's filepath contains the userPath, add it to the list of modules to delete
            if moduleFilePath.startswith(userPath):
                print("Removing %s" % key)
                toDelete.append(key)

        except:
            pass

    # If we'd deleted the module in the loop above, it would have changed the size of the dictionary and
    # broken the loop. So now we go over the list we made and delete all the modules
    for module in toDelete:
        del sys.modules[module]
