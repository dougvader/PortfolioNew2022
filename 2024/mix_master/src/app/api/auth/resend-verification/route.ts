import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { sendEmail } from '@/lib/email';

export async function POST(req: NextRequest) {
  const { email } = await req.json();

  if (!email) {
    return NextResponse.json({ error: 'Email is required' }, { status: 400 });
  }

  try {
    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    if (user.emailVerified) {
      return NextResponse.json({ error: 'Email is already verified' }, { status: 400 });
    }

    // Generate a new verification token
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

    return NextResponse.json({ message: 'Verification email resent successfully' }, { status: 200 });
  } catch (error) {
    console.error('Error resending verification email:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
