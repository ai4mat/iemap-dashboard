class urls:
    base_url = "https://ai4mat.enea.it"
    register = f"{base_url}/auth/register"
    login = f"{base_url}/auth/jwt/login"
    post_metadata = f"{base_url}/api/v1/project/add"
    post_file = f"{base_url}/api/v1/project/add/file/?project_id="
    query = f"{base_url}/api/v1/project/query/"
    get_user_projects_info = f"{base_url}/api/v1/user/projects/info"
