<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<% res = get_current_date() %>
<p>${res}</p>
    
<ol>
    % for task in objects:
    <pre><h1>${task.name|entity}</h1></pre>
    % if task.description:
    <h2>Task description:<h2><pre><h2>${task.description|entity}</h2></pre>
    % endif
    <h4>Task Information</h4>
    % if task.priority:
    <p>Priority: ${task.priority|entity}</p>
    % endif
    % if task.due_date:
    <p>Due date: ${formatLang(task.due_date, date=True)}</p>
    % endif
    % if task.due_time:
    <p>Lasts ${formatLang(task.due_time, digits=1)} hours</p>
    % endif
    % if task.user_id:
    <p>Assigned to ${task.user_id.name|entity}</p>
    % endif
    % if task.category_id:
    <p>Category ${task.category_id.complete_name|entity}</p>
    % endif
    
   	<p>State: ${task.state|entity}</p>
    
    % endfor
</ol>
</body>
</html>