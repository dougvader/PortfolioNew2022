import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  service: 'Gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS, // Use the app-specific password here
  },
  tls: {
    rejectUnauthorized: false, // Add this line to allow self-signed certificates
  },
});

export async function sendEmail({ to, subject, text }: { to: string, subject: string, text: string }) {
  await transporter.sendMail({
    from: process.env.EMAIL_USER,
    to,
    subject,
    text,
  });
}