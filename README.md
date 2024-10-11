# Projectube Recommendation System
I design a recommendation system server using Flask for [Projectube](https://www.projectube.org/)
## Normal use
1. Clone
- Go to terminal
```
https://github.com/hoangcaobao/Projectube_Recommendation_System.git
```
2. Change directory:
```
cd Projectube_Recommendation_System
```
3. GraphQL DATABASE link:
```
export GRAPHQL=link
```
- REMEMBER NO SPACE BETWEEN GRAPHQL=yourlink

4. Install packages:
```
pip install -r requirements.txt
```

5. Run:
```
python3 wsgi.py
```
---
## Docker use
1. Clone
- Go to terminal
```
https://github.com/hoangcaobao/Projectube_Recommendation_System.git
```
2. Change directory:
```
cd Projectube_Recommendation_System
```
3. Docker build:
```
docker image build -t app .
```
4. Docker run:
```
docker run -e GRAPHQL=link -p 5000:5000 app
```
---
## HOANG CAO BAO
