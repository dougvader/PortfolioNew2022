import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcrypt';
import { sendEmail } from '@/lib/email'; // Assume you have a utility to send emails

export async function POST(req: NextRequest) {
  const { email, password } = await req.json();

  if (!email || !password) {
    return NextResponse.json({ error: 'Email and password are required' }, { status: 400 });
  }

  try {
    // Check if the user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      return NextResponse.json({ error: 'User already exists' }, { status: 409 });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
      data: {
        email,
        hashedPassword,
        emailVerified: new Date(0), // Set to epoch date to indicate not verified
      },
    });

    // Generate a confirmation token
    const token = await prisma.verificationToken.create({
      data: {
        identifier: email,
        token: require('crypto').randomBytes(32).toString('hex'),
        expires: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
      },
    });

    // Send confirmation email
    const confirmationUrl = `${process.env.NEXTAUTH_URL}/api/auth/confirm?token=${token.token}`;
    await sendEmail({
      to: email,
      subject: 'Confirm your email address',
      text: `Please confirm your email address by clicking the following link: ${confirmationUrl}`,
    });

    return NextResponse.json({ message: 'User created. Please check your email to confirm your address.' }, { status: 201 });
  } catch (error) {
    console.error('Error creating user:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}