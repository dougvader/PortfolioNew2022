import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const token = searchParams.get('token');

  if (!token) {
    return NextResponse.json({ error: 'Token is required' }, { status: 400 });
  }

  try {
    const verificationToken = await prisma.verificationToken.findUnique({
      where: { token },
    });

    if (!verificationToken || verificationToken.expires < new Date()) {
      return NextResponse.json({ error: 'Invalid or expired token' }, { status: 400 });
    }

    await prisma.user.update({
      where: { email: verificationToken.identifier },
      data: { emailVerified: true },
    });

    await prisma.verificationToken.delete({
      where: { token },
    });

    const baseUrl = process.env.NEXTAUTH_URL || 'http://localhost:3000';
    return NextResponse.redirect(`${baseUrl}/auth/confirmed`);
  } catch (error) {
    console.error('Error confirming email:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}