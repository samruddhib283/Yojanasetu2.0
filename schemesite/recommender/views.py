from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import SchemeRequest
import json
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector


import os
from dotenv import load_dotenv



def dashboard(request):
    my_requests = SchemeRequest.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'recommender/dashboard.html', {'requests': my_requests})

def index(request):
    return render(request, 'recommender/index.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))  # 🔁 Redirect to dashboard
    else:
        form = UserCreationForm()
    return render(request, 'recommender/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('dashboard'))  # 🔁 Redirect to dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'recommender/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import openai
import os
import json
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import openai
import os
import json
from dotenv import load_dotenv

def all_schemes(request):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="student@172005",
            database="schemes"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM schemes")
        schemes = cursor.fetchall()

        # Extract unique values
        ministries = sorted(set(s['ministry'] for s in schemes if s['ministry']))
        sectors = sorted(set(s['sector'] for s in schemes if s['sector']))
        years = sorted(set(str(s['launch_year']) for s in schemes if s['launch_year']))
        cs_types = sorted(set(s['cs_css'] for s in schemes if s['cs_css']))

        return render(request, 'recommender/all_schemes.html', {
            'schemes': schemes,
            'ministries': ministries,
            'sectors': sectors,
            'years': years,
            'cs_types': cs_types,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


import joblib
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def predict_scheme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            age = int(data.get("age"))
            income = int(data.get("income"))
            occupation = data.get("occupation").lower()

            # Load model and encoder
            base_dir = os.path.dirname(__file__)
            model = joblib.load(os.path.join(base_dir, 'model/scheme_model.pkl'))
            encoder = joblib.load(os.path.join(base_dir, 'model/occupation_encoder.pkl'))

            # Encode occupation
            occupation_encoded = encoder.transform([occupation])[0]

            # Prepare input
            X_test = [[age, age, income, income, occupation_encoded]]

            # Predict
            prediction = model.predict(X_test)

            return JsonResponse({"recommended_scheme": prediction[0]})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Only POST method allowed"}, status=400)


def recommend_scheme_page(request):
    return render(request, 'scheme_recommender.html')

import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key='AIzaSyAUxT_edNP0f7uYWXf9uiNghmAq9_Z2b3k')  # Replace with settings.GEMINI_API_KEY if using from settings

@csrf_exempt
def summarize_filtered_schemes(request):
    if request.method == 'POST':
        ministry = request.POST.get('ministry', '')
        sector = request.POST.get('sector', '')
        year = request.POST.get('year', '')
        cs_css = request.POST.get('cs_css', '')

        # Example: Fetching filtered schemes from your database
        from .models import Scheme
        schemes = Scheme.objects.all()
        if ministry:
            schemes = schemes.filter(ministry=ministry)
        if sector:
            schemes = schemes.filter(sector=sector)
        if year:
            schemes = schemes.filter(launch_year=year)
        if cs_css:
            schemes = schemes.filter(cs_css=cs_css)

        if not schemes.exists():
            return JsonResponse({'summary': 'No summaries available for selected filters.'})

        # Prepare input for Gemini
        prompt = "\n\n".join([f"{s.name}: {s.summary}" for s in schemes])
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Summarize the following government schemes with:\n- Overview\n- Key Benefits\n- Eligibility Criteria\n- Application Process\n\nSchemes:\n{prompt}")

        return JsonResponse({'summary': response.text})
    return JsonResponse({'summary': 'Invalid request method.'})
def chatbot_view(request):
    return render(request, 'recommender/chatbot.html')

#video guide
def video_guides(request):
    # Example dummy data; replace with DB data
    schemes = [
        {"name": "PM-Kisan", "description": "Income support to farmers", "youtube_id": "https://youtu.be/eaD5iRiTh94?si=8e9uyQbNGhVEb6LU"},
        {"name": "Startup India", "description": "Support for entrepreneurs", "youtube_id": "fCz2x-NFK10"},
        # Add up to 20
    ]
    return render(request, "recommender/video_guides.html", {"schemes": schemes})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import openai
from dotenv import load_dotenv
from .models import SchemeHistory

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@csrf_exempt
def chatgpt_scheme_recommender(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            scheme = data.get("scheme")
            help_type = data.get("help_type").lower()

            base_prompt = f"""
You are an assistant for Indian Government schemes. A user wants help with the scheme: "{scheme}".
They need: "{help_type}"

Provide:
"""

            if "youtube" in help_type:
                # Return YouTube link instead of text response
                query = f"How to apply for {scheme} scheme"
                youtube_url = f"https://www.youtube.com/embed?listType=search&list={query.replace(' ', '+')}"
                return JsonResponse({"type": "youtube", "video_url": youtube_url})
            else:
                query_prompt = base_prompt + {
                    "step": "Step-by-step guide to apply for the scheme.",
                    "guide": "Step-by-step guide to apply.",
                    "documents": "List of required documents.",
                    "deadlines": "Deadlines or timelines to apply.",
                    "contact": "Contact details of helpline, phone number, or email."
                }.get(help_type, "Relevant information.")

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for Indian government scheme queries."},
                        {"role": "user", "content": query_prompt}
                    ],
                    max_tokens=400
                )
                reply = response.choices[0].message.content.strip()
                return JsonResponse({"type": "text", "response": reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
