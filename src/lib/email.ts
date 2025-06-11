import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export interface DemoRequestEmailData {
  firstName: string
  lastName: string
  email: string
  phone?: string
  jobTitle: string
  organizationName: string
  organizationType: string
  organizationSize: string
  currentECGSystem?: string
  primaryUseCase: string
  interestedFeatures: string[]
  timeframe: string
  preferredDemoType: string
  additionalRequirements?: string
  country: string
}

export interface ContactInquiryEmailData {
  firstName: string
  lastName: string
  email: string
  company?: string
  inquiryType: string
  subject: string
  message: string
}

export async function sendDemoRequestConfirmation(data: DemoRequestEmailData) {
  try {
    const { data: emailData, error } = await resend.emails.send({
      from: process.env.EMAIL_FROM || 'noreply@hearline.dz',
      to: [data.email],
      subject: 'Demo Request Confirmation - Hearline AI',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2563eb; margin: 0;">Hearline AI</h1>
            <p style="color: #666; margin: 5px 0;">Advanced Cardiac AI Solutions</p>
          </div>
          
          <h2 style="color: #333; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">Demo Request Confirmed</h2>
          
          <p>Dear ${data.firstName} ${data.lastName},</p>
          
          <p>Thank you for your interest in Hearline AI! We've received your demo request and our team will contact you within 24 hours to schedule your personalized demonstration.</p>
          
          <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #2563eb; margin-top: 0;">Your Demo Request Details:</h3>
            <ul style="list-style: none; padding: 0;">
              <li style="margin: 8px 0;"><strong>Organization:</strong> ${data.organizationName}</li>
              <li style="margin: 8px 0;"><strong>Role:</strong> ${data.jobTitle}</li>
              <li style="margin: 8px 0;"><strong>Primary Use Case:</strong> ${data.primaryUseCase}</li>
              <li style="margin: 8px 0;"><strong>Implementation Timeframe:</strong> ${data.timeframe}</li>
              <li style="margin: 8px 0;"><strong>Interested Features:</strong> ${data.interestedFeatures.join(', ')}</li>
            </ul>
          </div>
          
          <div style="background: #dbeafe; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #1d4ed8; margin-top: 0;">What Happens Next?</h3>
            <ul style="margin: 0; padding-left: 20px;">
              <li>Our specialist will review your requirements</li>
              <li>Schedule a 30-minute personalized demo session</li>
              <li>Customize the demonstration to your specific needs</li>
              <li>Q&A session with our cardiac AI experts</li>
            </ul>
          </div>
          
          <p>If you have any immediate questions, feel free to reach out to us at <a href="mailto:demo@hearline.dz" style="color: #2563eb;">demo@hearline.dz</a> or call us at +213 XXX XXX XXX.</p>
          
          <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
            <p style="color: #666; font-size: 14px;">
              Best regards,<br>
              The Hearline AI Team<br>
              <a href="https://hearline.dz" style="color: #2563eb;">hearline.dz</a>
            </p>
          </div>
        </div>
      `,
    })

    if (error) {
      console.error('Failed to send demo confirmation email:', error)
      throw new Error('Failed to send confirmation email')
    }

    return { success: true, messageId: emailData?.id }
  } catch (error) {
    console.error('Email service error:', error)
    throw error
  }
}

export async function sendDemoRequestNotification(data: DemoRequestEmailData) {
  try {
    const { data: emailData, error } = await resend.emails.send({
      from: process.env.EMAIL_FROM || 'noreply@hearline.dz',
      to: [process.env.ADMIN_EMAIL || 'admin@hearline.dz'],
      subject: `New Demo Request - ${data.organizationName}`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #dc2626; margin: 0;">🚨 New Demo Request</h1>
          </div>
          
          <div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 20px; margin: 20px 0;">
            <h2 style="color: #dc2626; margin-top: 0;">Demo Request from ${data.firstName} ${data.lastName}</h2>
            <p><strong>Organization:</strong> ${data.organizationName}</p>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Role:</strong> ${data.jobTitle}</p>
          </div>
            <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Request Details:</h3>
            <table style="width: 100%; border-collapse: collapse;">
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Phone:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.phone || 'Not provided'}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Organization Type:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.organizationType}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Organization Size:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.organizationSize}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Current ECG System:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.currentECGSystem || 'Not specified'}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Primary Use Case:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.primaryUseCase}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Timeframe:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.timeframe}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Preferred Demo Type:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.preferredDemoType}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Features:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.interestedFeatures.join(', ')}</td></tr>
              <tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Country:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.country}</td></tr>
              ${data.additionalRequirements ? `<tr><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;"><strong>Additional Requirements:</strong></td><td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">${data.additionalRequirements}</td></tr>` : ''}
            </table>
          </div>
          
          <div style="text-align: center; margin: 30px 0;">
            <p style="background: #fbbf24; color: #92400e; padding: 15px; border-radius: 8px; font-weight: bold;">
              ⚡ Action Required: Contact within 24 hours
            </p>
          </div>
        </div>
      `,
    })

    if (error) {
      console.error('Failed to send demo notification email:', error)
      throw new Error('Failed to send notification email')
    }

    return { success: true, messageId: emailData?.id }
  } catch (error) {
    console.error('Email service error:', error)
    throw error
  }
}

export async function sendContactInquiryConfirmation(data: ContactInquiryEmailData) {
  try {
    const { data: emailData, error } = await resend.emails.send({
      from: process.env.EMAIL_FROM || 'noreply@hearline.dz',
      to: [data.email],
      subject: 'Message Received - Hearline AI Support',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2563eb; margin: 0;">Hearline AI</h1>
            <p style="color: #666; margin: 5px 0;">Advanced Cardiac AI Solutions</p>
          </div>
          
          <h2 style="color: #333; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">Message Received</h2>
          
          <p>Dear ${data.firstName} ${data.lastName},</p>
          
          <p>Thank you for contacting Hearline AI! We've received your message and our team will get back to you within 24 hours.</p>
          
          <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #2563eb; margin-top: 0;">Your Message Details:</h3>
            <ul style="list-style: none; padding: 0;">
              <li style="margin: 8px 0;"><strong>Inquiry Type:</strong> ${data.inquiryType}</li>
              <li style="margin: 8px 0;"><strong>Subject:</strong> ${data.subject}</li>
              ${data.company ? `<li style="margin: 8px 0;"><strong>Organization:</strong> ${data.company}</li>` : ''}
            </ul>
            <div style="background: #fff; padding: 15px; border-radius: 6px; margin-top: 15px;">
              <strong>Message:</strong><br>
              <p style="margin: 10px 0;">${data.message}</p>
            </div>
          </div>
          
          <div style="background: #dbeafe; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #1d4ed8; margin-top: 0;">What Happens Next?</h3>
            <ul style="margin: 0; padding-left: 20px;">
              <li>Our team will review your inquiry</li>
              <li>You'll receive a personalized response within 24 hours</li>
              <li>For urgent matters, call +213 XXX XXX XXX</li>
            </ul>
          </div>
          
          <p>For immediate assistance, you can also reach us at <a href="mailto:support@hearline.dz" style="color: #2563eb;">support@hearline.dz</a>.</p>
          
          <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
            <p style="color: #666; font-size: 14px;">
              Best regards,<br>
              The Hearline AI Support Team<br>
              <a href="https://hearline.dz" style="color: #2563eb;">hearline.dz</a>
            </p>
          </div>
        </div>
      `,
    })

    if (error) {
      console.error('Failed to send contact confirmation email:', error)
      throw new Error('Failed to send confirmation email')
    }

    return { success: true, messageId: emailData?.id }
  } catch (error) {
    console.error('Email service error:', error)
    throw error
  }
}

export async function sendContactInquiryNotification(data: ContactInquiryEmailData) {
  try {
    const { data: emailData, error } = await resend.emails.send({
      from: process.env.EMAIL_FROM || 'noreply@hearline.dz',
      to: [process.env.ADMIN_EMAIL || 'admin@hearline.dz'],
      subject: `New Contact Inquiry - ${data.inquiryType}`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
          <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #dc2626; margin: 0;">📧 New Contact Inquiry</h1>
          </div>
          
          <div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 20px; margin: 20px 0;">
            <h2 style="color: #dc2626; margin-top: 0;">Message from ${data.firstName} ${data.lastName}</h2>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Inquiry Type:</strong> ${data.inquiryType}</p>
            <p><strong>Subject:</strong> ${data.subject}</p>
            ${data.company ? `<p><strong>Organization:</strong> ${data.company}</p>` : ''}
          </div>
          
          <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Message:</h3>
            <div style="background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e5e7eb;">
              ${data.message}
            </div>
          </div>
          
          <div style="text-align: center; margin: 30px 0;">
            <p style="background: #fbbf24; color: #92400e; padding: 15px; border-radius: 8px; font-weight: bold;">
              ⚡ Action Required: Respond within 24 hours
            </p>
          </div>
        </div>
      `,
    })

    if (error) {
      console.error('Failed to send contact notification email:', error)
      throw new Error('Failed to send notification email')
    }

    return { success: true, messageId: emailData?.id }
  } catch (error) {
    console.error('Email service error:', error)
    throw error
  }
}
