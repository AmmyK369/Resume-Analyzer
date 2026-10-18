def normalize(skill:str)->str:
    return skill.strip().lower()

def calculate_score(resume_skills:list[str],required_skills: list[str]) -> dict:
    resume_set={normalize (s) for s in resume_skills}
    required_set={normalize(s) for s in required_skills}
    
    if not required_set:
        return{"score":0, "matched":[], "missing":[]}
    
    matched= resume_set & required_set #intersection
    missing= required_set - resume_set #difference from 1  minus 2
    
    score = round(len(matched) / len(required_set) * 100)
    
    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
    }
    