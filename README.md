# Progress
This is a management tool, focused on communicating project progress and receiving feedback.

See this project [online in pythonanywhere](https://keinermendoza.pythonanywhere.com)

![this project](https://github.com/keinermendoza/project-managment/assets/75821986/651f1986-0107-49b3-b2bd-f027b0e1851f)

## Get Started

Create a virtual enviorment
```
python3 -m venv venv
```

Activate the virtual enviorment
```
source venv/bin/activate
```

go into the project folder

```
cd progress
```

Install the denpendencies

```
pip install -r requirements.txt
```

create migrations
```
python3 manage.py makemigrations progress
python3 manage.py makemigrations account
```

apply migrations

```
python3 manage.py migrate
```


run the development server

```
python3 manage.py runserver
```


## **Admin**

Important actions such as creating projects, tasks and editing user permissions are possible only through the admin.

The editing is done through the integrated Django forms, the configuration for admin is in:

```
📁 progress/admin.py
```

### **Tasks**


Tasks have an estimated completion period that must be declared when created. When a task is marked as *"Working on it"* the property **"get_time_to_finish"** is calculated showing the time in which the task should be ready, in case the status of the task is marked as *"Completed"* or as *"Waiting feed back"* the value of this property will be set to None.

<details>
  <summary> 📽️ See Demo</summary>

![automatic calculation time for finish task](https://github.com/keinermendoza/project-managment/assets/75821986/db749ab1-3af3-4eb3-ac97-a2909aea46b9)

</details>
<br>


### **Project Privacy**

The **Project** model has a *"Public"* property that allows sharing a project with all registered users regardless of whether they are assigned to said project. If this property is set to False, only users assigned to the project will be able to interact with it.

### **Notes**



When creating a note from the admin it is not necessary to mark the user, the current user is detected. If a note is edited, the original user is maintained.

<details>
  <summary> 📽️ See Demo</summary>
  
![auto save user for admin notes](https://github.com/keinermendoza/project-managment/assets/75821986/7e6e9703-d6ba-4c16-8007-3a2de480c972)

</details>
<br>

### **Views**



I added a custom view to the admin that allows you to view the project information in a unified way. This is registered within the progress application.

<details>
  <summary> 📽️ See Demo</summary>

![custom_admin_view](https://github.com/keinermendoza/project-managment/assets/75821986/03cc173e-0069-4a4b-adee-fd35446759c8)

</details>
<br>


## **Technology Stack**

🚀 [Django](#Django)

🚀 [Alpinejs](#alpinejs)

🚀 [HTMX](#htmx)

🚀 Tailwindcss

### **Django**

The Backend is completely managed by django, using the django template engine to generate HTML on the server, no Json responses are used. The validation of the requests is done with django forms.

In addition to the typical Django stuff, I added a couple of third-party apps:

**[django-htmx](https://django-htmx.readthedocs.io/en/latest/)**


+ [request.htmx (__bool__)](https://django-htmx.readthedocs.io/en/latest/middleware.html#django_htmx.middleware.HtmxDetails.__bool__)

it provides a way to differentiate requests made on htmx, in which case I can respond with a partial instead of a complete page.

+ [django_htmx.http.retarget](https://django-htmx.readthedocs.io/en/latest/http.html#django_htmx.http.retarget)  
+ [django_htmx.http.HttpResponseLocation](https://django-htmx.readthedocs.io/en/latest/http.html#django_htmx.http.HttpResponseLocation)

I use them in the home view because in this case I want to render the entire page. to show things like the name of the user who has logged in.

**[django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)**

I used it and it has a way to put the CSS classes directly into the HTML. This is important because I needed tailwindcss to be able to access these classes during development.

### **[Alpinejs](https://alpinejs.dev/)**

+ [x-data](https://alpinejs.dev/directives/data)

provides a way to relate data to HTML elements that have a local scope, being available only within the element in which they are defined. the library parses the html content upon startup on the client. This gives some freedom when creating the html, for example:


In the next file are two sections in both of which I define a series of local variables:
``` 
📁  templates/progress/project_detail.html 
```
I used the next line for define the variables

``` javascript
x-data="{Modalvisible:false, noteCount: {{note_count}}, editing:false}"
```

These variables are used to maintain the note count and adjust the visibility of a modal. Because the behavior of modal and count variables is very similar, I defined such a section in another html document that I added to both sections via the tag {% include %}

<details>
  <summary> 📽️ See Demo update counter</summary>

![update_counter](https://github.com/keinermendoza/project-managment/assets/75821986/6595ceef-b333-4733-88ac-d39a57971951)

</details>
<br>

Within that document I can manage the defined variables and although it is a single document, the locality of the definition will mean that they are different variables in the client.


+ [Alpine.store](https://alpinejs.dev/magics/store)

This allows me to store objects including methods that can be accessed or executed by locally accessible alpine scripts.
I mainly used it to establish which section of the navigation bar was active. You can see its use in:

```
📁  progress/static/progress/js/alpinestore.js
📁  progress/templates/progress/snippets/btn_section.html
```


### **[HTMX](https://htmx.org/docs/)**

most of this project uses htmx as a way to send request and receive responses. From that I would like to highlight the use of verbs that in some cases is essential to determine how to handle the server-side response, such as the edit Note form that is in notelist_modal:

```html
<form x-show="editing"
    @set-editing-false="editing = false" 
    . . .                    

{% if project_notes %}
    . . .
    hx-put="{% url 'progress:create_project_note' object.id %}"
{% else %}
    . . .
    hx-put="{% url 'progress:create_task_note' object.id %}"
{% endif %}

    class="form-edit-notes w-full relative"> . . . </form>
```
Another very interesting thing is the way in which an action can be executed after triggering an event with htmx. In the case of this project I integrated [SweetAlert](https://sweetalert2.github.io/#usage) alerts with certain htmx requests, you can see the code in:

```
📁  progress/static/progress/js/alpinestore.js
```

## Collaborations

I did this project alone, but it is totally open to collaborations, improvements and modifications. The only conditions are to maintain the [technology stack](#technologies-stack).

