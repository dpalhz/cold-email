import openai
import json
import logging
from django.conf import settings
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

logger = logging.getLogger(__name__)

# Set OpenAI API key and initialize OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


@staff_member_required(login_url='/auth/login/')
def generator_view(request):
    return render(request, "generator.html")

def send_to_openai(user_input):
    company_background = """Algo's Network adalah perusahaan agency yang bertujuan untuk memberikan solusi 
    kepada business dengan memberikan layanan mengenai Data & AI Solutions, Digital Marketing, Software, 
    Management Consulting, Media Production. Tujuan dari Algo's Network adalah membantu penerapan transformasi 
    digital pada bisnis."""

    tone = user_input['mode']

    if user_input['sendto'] == 'Customers':
        audience_desc = "Customer perusahaan Algo's Network, yaitu pemilik bisnis, petinggi perusahaan, dan sejenisnya."
        tone = "Gunakan kata-kata persuasif sesuai best practice dalam marketing & copywriting."

    else:
        audience_desc = "Karyawan perusahaan Algo's Network"
    prompt_text = f"""
    {company_background}

    Anda adalah asisten terbaik di Algo's Network. Buatkan konten email (tanpa subject) yang sesuai dengan detail berikut,

    Subject email: {user_input['subject']}

    Audiens: {audience_desc}

    Gaya dan Tone bahasa: {tone}

    Detail dan konteks email: {user_input['email_detail']}

    Bahasa: {user_input['language']}

    Keterangan tambahan:
    1. Gunakan bulletpoints jika diperlukan.
    2. Berikan bahasa yang concise, namun tetap memberikan pesan yang kuat
    3. Berikan keterangan Algo's Network sebagai sender di bagian bawah email
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ],
        stream=True
    )

    return response

@staff_member_required(login_url='/auth/login/')
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message')  
            if user_input:
                response = send_to_openai(user_input)
                def generate():
                    for chunk in response:
                        for choice in chunk.choices:
                            content = choice.delta.content
                            yield content
                return StreamingHttpResponse(generate(), content_type='text/plain')
        except Exception as e:
            logger.error("Error processing request: %s", e)
            return JsonResponse({'response': 'Error processing request'}, status=500)
    return JsonResponse({'response': 'Invalid request'}, status=400)

from sendingemail.forms import EmailScheduleForm

@staff_member_required(login_url='/auth/login/')
def generator_view(request):
    form = EmailScheduleForm()
    return render(request, 'generator.html', {'form': form})