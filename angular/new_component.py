import os
from sys import argv

url = '../src/app/'
new_component = argv[1]

need_dirs = ['controllers', 'models', 'views', 'styles']

if not os.path.exists(url+'controllers'): 
    for folder in need_dirs: os.mkdir(url+folder)

controller_text = '''import { Component } from '@angular/core';

@Component({
    selector: 's-*',
    templateUrl: '../views/*.component.html',
    styleUrls: ['../styles/*.component.sass']
})
export class *Component {}
'''

view_text = '''<h3>* component default view</h3>'''

with open(os.path.join(url,need_dirs[0],'{}.component.ts'.format(new_component)), 'w') as f:
    f.write(controller_text.replace('*', new_component))

with open(os.path.join(url,need_dirs[2],'{}.component.html'.format(new_component)), 'w') as f:
    f.write(view_text.replace('*', new_component))

with open(os.path.join(url,need_dirs[3],'{}.component.sass'.format(new_component)), 'w') as f: 
    f.close()

if not os.path.isfile(url+'components.ts'): 
    print('hello')
    with open(os.path.join(url+'components.ts'), 'w') as f:
        f.write("export { AppComponent as Base } from './app.component'")

with open(os.path.join(url,'components.ts'), 'a') as f:
    f.write("\nexport { %sComponent as %s } from './controllers/%s.component'\n" % (new_component, new_component, new_component))

with open(os.path.join(url, 'app.module.ts'), 'r+') as f:
    text = f.readlines()

    if '//' not in text[0]:
        text.insert(0, '//begin of auto imports from new_component.py\n')
        text.insert(1,'// end auto imported\n')

    text.insert(1, "import { %sComponent } from './controllers/%s.component'\n" % (new_component, new_component))
    
    for index, line in enumerate(text): 
        if 'declarations' in line:
            text.insert(index+1, '\t{}Component, // auto imported component\n'.expandtabs(4).format(new_component))
                

    f.seek(0)
    f.writelines(text)

