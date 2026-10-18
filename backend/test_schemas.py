from schemas import ResumeData

good='{"skills":["C++","Python"],"education":"B.Tech CSE"}'
bad= '{"skills":5,"education":"B.Tech CSE"}'

print(ResumeData.model_validate_json(good))
print(ResumeData.model_validate_json(bad))

