
    def flat_dict(original):
 
        flat_items = []
        stack = list(original.items())
        visited = set()
        while (stack):
            root_key, root_val = stack.pop()
            if isinstance(root_val, dict):
                if root_key not in visited:
                    kv_pairs = []
                    for child_key, child_val in root_val.items():
                        kv_pairs.append((root_key + '.' + child_key, child_val))
                        # If there is any confict with multiple keys uncomment below
                        # kv_pairs.append((root_key + '.' + str(uuid.uuid4()) + '.' + child_key, v))
                    stack.extend(kv_pairs)

            elif isinstance(root_val, list):
                for vdict in root_val:
                    if root_key not in visited:
                        kv_pairs = []
                        for child_key, child_val in vdict.items():
                            kv_pairs.append((root_key + '.' + child_key, child_val))
                            # If there is any confict with multiple keys uncomment below
                            # kv_pairs.append((root_key + '.' + str(uuid.uuid4()) + '.' + child_key, v))
                        stack.extend(kv_pairs)
            else:
                flat_items.append(list((root_key, root_val)))
            visited.add(root_key)
        return dict(flat_items)
