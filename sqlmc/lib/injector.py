class Injector:
    @staticmethod
    def inject(url):
        query_start = url.find('?')
        if query_start == -1:
            return url

        base_url = url[:query_start]
        query_string = url[query_start+1:]
        params = query_string.split('&')

        modified_params = []
        for param in params:
            key_value = param.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                # Add single quotes around the value
                modified_value = f"{value}'"
                modified_params.append(f"{key}={modified_value}")
            else:
                modified_params.append(param)

        modified_query_string = '&'.join(modified_params)
        modified_url = f"{base_url}?{modified_query_string}"

        return modified_url
