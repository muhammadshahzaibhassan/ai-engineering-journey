def get_members(group):
    # Sample data structure for demonstration
    groups = {
        "sales": ["Alice", "Bob", "Charlie"],
        "engineering": ["David", {"group": "frontend"}, {"group": "backend"}, "Eve", "Frank"],
        "everyone": ["Grace", {"group": "sales"}, {"group": "engineering"}, "Henry", "Ivy", "Jack"]
    }
    
    members = groups.get(group, [])
    result = []
    for member in members:
        if isinstance(member, dict) and "group" in member:
            result.append(member["group"])
        else:
            result.append(member)
    return result

def is_group(member):
    return isinstance(member, str) and member in ["sales", "engineering", "frontend", "backend", "everyone"]

def count_users(group):
    count = 0
    for member in get_members(group):
        if is_group(member):
            count += count_users(member)
        else:
            count += 1
    return count


print(count_users("sales"))        # Should be 3
print(count_users("engineering"))  # Should be 8
print(count_users("everyone"))     # Should be 18