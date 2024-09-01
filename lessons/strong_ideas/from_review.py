def before():
    if company_id == subcontractor.id:
        for restricted_field in ["rejected_reason", "responded_comment"]:
            if restricted_field in data:
                return {restricted_field: f"subcontractor is not allowed to set {restricted_field}"}
            
def after():
    # if company_id == subcontractor.id and set(data).intersection({"rejected_reason", "responded_comment"}):
    #     return {restricted_field: f"subcontractor is not allowed to set {restricted_field}"}
    if company_id == subcontractor.id and (
        restricted_fields := set(data).intersection({"rejected_reason", "responded_comment"})
    ):
        return f"subcontractor is not allowed to set {restricted_fields}"
        