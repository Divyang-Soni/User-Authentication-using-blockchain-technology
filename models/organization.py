class OrganizationDetails:
    id = None
    name = None
    address_line_1 = None
    city = None
    state = None
    country = None
    zip = None
    phone = None
    headquarter = None
    founded_date = None
    organization_type = None
    created_date = None
    created_by = None
    modified_date = None
    modified_by = None
    delete_flag = None
    deleted_by = None


class OrganizationBranch:
    id = None
    organization_id = None
    address_line_1 = None
    city = None
    state = None
    country = None
    zip = None
    phone = None
    created_date = None
    created_by = None
    modified_date = None
    modified_by = None
    delete_flag = None
    deleted_by = None


class OrganizationType:
    id = None
    type = None
    delete_flag = None
