from pytaurus import Project


path = '/path/to/TCAD/project'
project = Project(path)

exit_code = project.run()
print(f'Project run with exit code {exit_code}')

exit_code = project.clean()
print(f'Project clean with exit code {exit_code}')
