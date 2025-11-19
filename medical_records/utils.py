from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from django.conf import settings
import os
from datetime import datetime

def generate_prescription_pdf(prescription_instance, file_path):
    """
    Gera o PDF da receita médica usando reportlab.
    """
    
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    styles = getSampleStyleSheet()
    Story = []

    # --- Cabeçalho (Dados do Médico) ---
    doctor = prescription_instance.doctor
    doctor_info = [
        Paragraph(f"<b>Dr(a). {doctor.user.get_full_name()}</b>", styles['h2']),
        Paragraph(f"CRM: {doctor.crm} - {doctor.crm_state}", styles['Normal']),
        Paragraph(f"Especialidade: {doctor.specialty}", styles['Normal']),
        Paragraph(f"Telefone: {doctor.user.phone or 'N/A'}", styles['Normal']),
        Spacer(1, 0.5*cm)
    ]
    Story.extend(doctor_info)

    # --- Título ---
    Story.append(Paragraph("<b>RECEITUÁRIO MÉDICO</b>", styles['h1']))
    Story.append(Spacer(1, 0.5*cm))

    # --- Dados do Paciente ---
    patient = prescription_instance.patient
    patient_info = [
        Paragraph(f"<b>Paciente:</b> {patient.user.get_full_name()}", styles['Normal']),
        Paragraph(f"<b>Data de Nascimento:</b> {patient.user.birth_date.strftime('%d/%m/%Y') if patient.user.birth_date else 'N/A'}", styles['Normal']),
        Paragraph(f"<b>CPF:</b> {patient.user.cpf}", styles['Normal']),
        Spacer(1, 0.5*cm)
    ]
    Story.extend(patient_info)

    # --- Medicamentos ---
    Story.append(Paragraph("<b>MEDICAMENTOS PRESCRITOS:</b>", styles['h3']))
    medications_text = prescription_instance.medications.replace('\n', '<br/>')
    Story.append(Paragraph(medications_text, styles['Normal']))
    Story.append(Spacer(1, 0.5*cm))

    # --- Instruções ---
    if prescription_instance.instructions:
        Story.append(Paragraph("<b>INSTRUÇÕES DE USO:</b>", styles['h3']))
        instructions_text = prescription_instance.instructions.replace('\n', '<br/>')
        Story.append(Paragraph(instructions_text, styles['Normal']))
        Story.append(Spacer(1, 0.5*cm))

    # --- Data e Validade ---
    Story.append(Paragraph(f"<b>Data da Emissão:</b> {prescription_instance.created_at.strftime('%d/%m/%Y')}", styles['Normal']))
    if prescription_instance.valid_until:
        Story.append(Paragraph(f"<b>Válida até:</b> {prescription_instance.valid_until.strftime('%d/%m/%Y')}", styles['Normal']))
    else:
        Story.append(Paragraph("<b>Validade:</b> Indeterminada", styles['Normal']))
    Story.append(Spacer(1, 2*cm))

    # --- Assinatura (Espaço) ---
    Story.append(Paragraph("___________________________________________________", styles['Normal']))
    Story.append(Paragraph(f"Assinatura e Carimbo do Dr(a). {doctor.user.get_full_name()}", styles['Normal']))
    
    doc.build(Story)
    return file_path
