def is_operator(user):
    return user.groups.filter(name="operator").exists()
