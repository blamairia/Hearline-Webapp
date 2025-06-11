import nodemailer from 'nodemailer'

// SMTP Email Service using the configured SMTP server
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT || '587'),
  secure: process.env.SMTP_PORT === '465', // true for 465, false for other ports
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
  tls: {
    rejectUnauthorized: false // For development/testing
  }
})

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

export interface DemoConfirmationEmailData {
  firstName: string
  lastName: string
  email: string
  organizationName: string
  preferredDemoType: string
  timeframe: string
  interestedFeatures: string[]
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

export async function sendContactInquiryConfirmation(data: ContactInquiryEmailData) {
  const { firstName, lastName, email, company, inquiryType, subject, message } = data

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank you for contacting Hearline AI</title>
      </head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <h1 style="color: #2563eb; margin-bottom: 10px;">Hearline AI</h1>
          <p style="color: #666; font-size: 16px;">Advanced ECG Analysis & Patient Monitoring</p>
        </div>
        
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
          <h2 style="color: #1e40af; margin-bottom: 20px;">Thank you for reaching out!</h2>
          <p>Dear ${firstName} ${lastName},</p>
          <p>We've received your inquiry and our team will get back to you within 24 hours.</p>
          
          <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <h3 style="color: #374151; margin-bottom: 15px;">Your Inquiry Details:</h3>
            <p><strong>Subject:</strong> ${subject}</p>
            <p><strong>Inquiry Type:</strong> ${inquiryType}</p>
            ${company ? `<p><strong>Company:</strong> ${company}</p>` : ''}
            <p><strong>Message:</strong></p>
            <div style="background-color: #f9fafb; padding: 15px; border-left: 4px solid #2563eb; margin-top: 10px;">
              ${message}
            </div>
          </div>
          
          <p>If you have any urgent questions, please don't hesitate to contact us directly.</p>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 14px;">
          <p>Best regards,<br>The Hearline AI Team</p>
          <p style="margin-top: 20px;">
            <a href="mailto:support@hearline.ai" style="color: #2563eb;">support@hearline.ai</a> | 
            <a href="https://hearline.ai" style="color: #2563eb;">hearline.ai</a>
          </p>
        </div>
      </body>
    </html>
  `

  const textContent = `
Thank you for contacting Hearline AI!

Dear ${firstName} ${lastName},

We've received your inquiry and our team will get back to you within 24 hours.

Your Inquiry Details:
Subject: ${subject}
Inquiry Type: ${inquiryType}
${company ? `Company: ${company}` : ''}
Message: ${message}

If you have any urgent questions, please don't hesitate to contact us directly.

Best regards,
The Hearline AI Team

support@hearline.ai | hearline.ai
  `

  const mailOptions = {
    from: `"Hearline AI" <${process.env.SMTP_USER}>`,
    to: email,
    subject: 'Thank you for contacting Hearline AI',
    text: textContent,
    html: htmlContent,
  }

  return await transporter.sendMail(mailOptions)
}

export async function sendContactInquiryNotification(data: ContactInquiryEmailData) {
  const { firstName, lastName, email, company, inquiryType, subject, message } = data

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Inquiry - Hearline AI</title>
      </head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <h1 style="color: #dc2626; margin-bottom: 10px;">New Contact Inquiry</h1>
          <p style="color: #666; font-size: 16px;">Hearline AI Admin Panel</p>
        </div>
        
        <div style="background-color: #fef2f2; padding: 30px; border-radius: 8px; margin-bottom: 30px; border-left: 4px solid #dc2626;">
          <h2 style="color: #991b1b; margin-bottom: 20px;">Contact Details</h2>
          
          <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p><strong>Name:</strong> ${firstName} ${lastName}</p>
            <p><strong>Email:</strong> <a href="mailto:${email}" style="color: #2563eb;">${email}</a></p>
            ${company ? `<p><strong>Company:</strong> ${company}</p>` : ''}
            <p><strong>Inquiry Type:</strong> ${inquiryType}</p>
            <p><strong>Subject:</strong> ${subject}</p>
            <p><strong>Timestamp:</strong> ${new Date().toLocaleString()}</p>
          </div>
          
          <div style="background-color: white; padding: 20px; border-radius: 6px;">
            <h3 style="color: #374151; margin-bottom: 15px;">Message:</h3>
            <div style="background-color: #f9fafb; padding: 15px; border-left: 4px solid #2563eb;">
              ${message}
            </div>
          </div>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 14px;">
          <p>Please respond to this inquiry promptly.</p>
          <p style="margin-top: 20px;">
            <a href="mailto:${email}?subject=Re: ${subject}" style="background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reply to Customer</a>
          </p>
        </div>
      </body>
    </html>
  `

  const textContent = `
New Contact Inquiry - Hearline AI

Contact Details:
Name: ${firstName} ${lastName}
Email: ${email}
${company ? `Company: ${company}` : ''}
Inquiry Type: ${inquiryType}
Subject: ${subject}
Timestamp: ${new Date().toLocaleString()}

Message:
${message}

Please respond to this inquiry promptly.
  `

  const mailOptions = {
    from: `"Hearline AI System" <${process.env.SMTP_USER}>`,
    to: process.env.SMTP_USER, // Send notification to the admin email
    subject: `New Contact Inquiry: ${subject}`,
    text: textContent,
    html: htmlContent,
  }

  return await transporter.sendMail(mailOptions)
}

export async function sendDemoRequestConfirmation(data: DemoConfirmationEmailData) {
  const { firstName, lastName, email, organizationName, preferredDemoType, timeframe, interestedFeatures } = data

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo Request Confirmation - Hearline AI</title>
      </head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <h1 style="color: #2563eb; margin-bottom: 10px;">Hearline AI</h1>
          <p style="color: #666; font-size: 16px;">Advanced ECG Analysis & Patient Monitoring</p>
        </div>
        
        <div style="background-color: #f0f9ff; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
          <h2 style="color: #0369a1; margin-bottom: 20px;">Demo Request Confirmed!</h2>
          <p>Dear ${firstName} ${lastName},</p>
          <p>Thank you for requesting a demo of Hearline AI. We're excited to show you how our advanced ECG analysis platform can transform your cardiac care workflow.</p>
            <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <h3 style="color: #374151; margin-bottom: 15px;">Demo Request Details:</h3>
            <p><strong>Organization:</strong> ${organizationName}</p>
            <p><strong>Demo Type:</strong> ${preferredDemoType}</p>
            <p><strong>Timeframe:</strong> ${timeframe}</p>
            <p><strong>Interested Features:</strong> ${interestedFeatures.join(', ')}</p>
          </div>
          
          <p><strong>What happens next?</strong></p>
          <ul>
            <li>Our team will contact you within 24 hours to schedule your personalized demo</li>
            <li>We'll discuss your specific needs and use cases</li>
            <li>You'll see live demonstrations of our AI-powered ECG analysis</li>
            <li>We'll provide pricing and implementation details</li>
          </ul>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 14px;">
          <p>Best regards,<br>The Hearline AI Team</p>
          <p style="margin-top: 20px;">
            <a href="mailto:demos@hearline.ai" style="color: #2563eb;">demos@hearline.ai</a> | 
            <a href="https://hearline.ai" style="color: #2563eb;">hearline.ai</a>
          </p>
        </div>
      </body>
    </html>
  `

  const textContent = `
Demo Request Confirmed - Hearline AI

Dear ${firstName} ${lastName},

Thank you for requesting a demo of Hearline AI. We're excited to show you how our advanced ECG analysis platform can transform your cardiac care workflow.

Demo Request Details:
Organization: ${organizationName}
Demo Type: ${preferredDemoType}
Timeframe: ${timeframe}
Interested Features: ${interestedFeatures.join(', ')}

What happens next?
- Our team will contact you within 24 hours to schedule your personalized demo
- We'll discuss your specific needs and use cases
- You'll see live demonstrations of our AI-powered ECG analysis
- We'll provide pricing and implementation details

Best regards,
The Hearline AI Team

demos@hearline.ai | hearline.ai
  `

  const mailOptions = {
    from: `"Hearline AI" <${process.env.SMTP_USER}>`,
    to: email,
    subject: 'Demo Request Confirmed - Hearline AI',
    text: textContent,
    html: htmlContent,
  }

  return await transporter.sendMail(mailOptions)
}

export async function sendDemoRequestNotification(data: DemoRequestEmailData) {
  const { 
    firstName, 
    lastName, 
    email, 
    phone, 
    jobTitle, 
    organizationName, 
    organizationType,
    organizationSize,
    currentECGSystem,
    primaryUseCase,
    interestedFeatures,
    timeframe,
    preferredDemoType,
    additionalRequirements,
    country
  } = data

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Demo Request - Hearline AI</title>
      </head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <h1 style="color: #059669; margin-bottom: 10px;">New Demo Request</h1>
          <p style="color: #666; font-size: 16px;">Hearline AI Admin Panel</p>
        </div>
        
        <div style="background-color: #f0fdf4; padding: 30px; border-radius: 8px; margin-bottom: 30px; border-left: 4px solid #059669;">
          <h2 style="color: #047857; margin-bottom: 20px;">Contact Information</h2>
          
          <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p><strong>Name:</strong> ${firstName} ${lastName}</p>
            <p><strong>Email:</strong> <a href="mailto:${email}" style="color: #2563eb;">${email}</a></p>
            ${phone ? `<p><strong>Phone:</strong> ${phone}</p>` : ''}
            <p><strong>Job Title:</strong> ${jobTitle}</p>
            <p><strong>Country:</strong> ${country}</p>
            <p><strong>Timestamp:</strong> ${new Date().toLocaleString()}</p>
          </div>
          
          <h3 style="color: #047857; margin-bottom: 15px;">Organization Details</h3>
          <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p><strong>Organization:</strong> ${organizationName}</p>
            <p><strong>Type:</strong> ${organizationType}</p>
            <p><strong>Size:</strong> ${organizationSize}</p>
            ${currentECGSystem ? `<p><strong>Current ECG System:</strong> ${currentECGSystem}</p>` : ''}
          </div>
          
          <h3 style="color: #047857; margin-bottom: 15px;">Demo Requirements</h3>
          <div style="background-color: white; padding: 20px; border-radius: 6px; margin: 20px 0;">
            <p><strong>Primary Use Case:</strong> ${primaryUseCase}</p>
            <p><strong>Interested Features:</strong> ${interestedFeatures.join(', ')}</p>
            <p><strong>Timeframe:</strong> ${timeframe}</p>
            <p><strong>Preferred Demo Type:</strong> ${preferredDemoType}</p>
            ${additionalRequirements ? `
              <p><strong>Additional Requirements:</strong></p>
              <div style="background-color: #f9fafb; padding: 15px; border-left: 4px solid #2563eb;">
                ${additionalRequirements}
              </div>
            ` : ''}
          </div>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 14px;">
          <p>Please schedule this demo promptly based on the requested timeframe.</p>
          <p style="margin-top: 20px;">
            <a href="mailto:${email}?subject=Demo Scheduling - Hearline AI" style="background-color: #059669; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Contact Prospect</a>
          </p>
        </div>
      </body>
    </html>
  `

  const textContent = `
New Demo Request - Hearline AI

Contact Information:
Name: ${firstName} ${lastName}
Email: ${email}
${phone ? `Phone: ${phone}` : ''}
Job Title: ${jobTitle}
Country: ${country}
Timestamp: ${new Date().toLocaleString()}

Organization Details:
Organization: ${organizationName}
Type: ${organizationType}
Size: ${organizationSize}
${currentECGSystem ? `Current ECG System: ${currentECGSystem}` : ''}

Demo Requirements:
Primary Use Case: ${primaryUseCase}
Interested Features: ${interestedFeatures.join(', ')}
Timeframe: ${timeframe}
Preferred Demo Type: ${preferredDemoType}
${additionalRequirements ? `Additional Requirements: ${additionalRequirements}` : ''}

Please schedule this demo promptly based on the requested timeframe.
  `

  const mailOptions = {
    from: `"Hearline AI System" <${process.env.SMTP_USER}>`,
    to: process.env.SMTP_USER, // Send notification to the admin email
    subject: `New Demo Request: ${organizationName}`,
    text: textContent,
    html: htmlContent,
  }

  return await transporter.sendMail(mailOptions)
}
