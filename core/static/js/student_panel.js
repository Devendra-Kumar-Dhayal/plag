document.getElementById('your-work-btn').addEventListener('click', function() {
    document.getElementById('panel-title').textContent = 'Your Work';
    document.getElementById('file-list').innerHTML = '';
    {% for file in user_uploaded_files %}
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '{{ file.file.url }}';
    a.target = '_blank';
    a.textContent = '{{ file.file.name }}';
    li.appendChild(a);
    document.getElementById('file-list').appendChild(li);
    {% endfor %}
    
});

document.getElementById('global-work-btn').addEventListener('click', function() {
    document.getElementById('panel-title').textContent = 'Reports';
    document.getElementById('file-list').innerHTML = '';
    {% for file in all_uploaded_files %}
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '{{ file.file.url }}';
    a.target = '_blank';
    a.textContent = '{{ file.file.name }}';
    var span = document.createElement('span');
    span.textContent = 'Owner: {{ file.user.username }}';
    li.appendChild(a);
    li.appendChild(span);
    document.getElementById('file-list').appendChild(li);
    {% endfor %}
});