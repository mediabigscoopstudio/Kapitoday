import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/dash/index.html'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        <a aria-label="Register Order" class="btn btn-sm btn-primary" href="{% url 'create_order' %}">
            <i class="bi bi-plus-lg"></i> Create Manual Order
        </a>"""

new_code = """        <div class="d-flex align-items-center gap-2">
            <form method="GET" action="" id="timeFilterForm">
                <select name="time_filter" class="form-select form-select-sm" onchange="document.getElementById('timeFilterForm').submit()" style="min-width: 150px; font-weight: 500;">
                    <option value="today" {% if current_filter == 'today' %}selected{% endif %}>Today</option>
                    <option value="this_week" {% if current_filter == 'this_week' %}selected{% endif %}>This Week</option>
                    <option value="this_month" {% if current_filter == 'this_month' %}selected{% endif %}>This Month</option>
                    <option value="this_quarter" {% if current_filter == 'this_quarter' %}selected{% endif %}>This Quarter</option>
                    <option value="last_6_months" {% if current_filter == 'last_6_months' %}selected{% endif %}>Last 6 Months</option>
                    <option value="all" {% if current_filter == 'all' %}selected{% endif %}>All Time</option>
                </select>
            </form>
            <a aria-label="Register Order" class="btn btn-sm btn-primary" href="{% url 'create_order' %}">
                <i class="bi bi-plus-lg"></i> Create Manual Order
            </a>
        </div>"""

if "timeFilterForm" not in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched index dropdown.")
else:
    print("Already patched.")
