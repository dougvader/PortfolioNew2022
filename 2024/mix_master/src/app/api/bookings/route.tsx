import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';
import { getSession } from 'next-auth/react';

const prisma = new PrismaClient();

export async function GET(req: NextRequest) {
    const session = await getSession({ req });

    if (!session) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    try {
        const bookings = await prisma.booking.findMany({
            where: { userId: session.user.id },
        });
        return NextResponse.json({ bookings }, { status: 200 });
    } catch (error) {
        console.error('Error fetching bookings:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}

export async function POST(req: NextRequest) {
    const { date, type } = await req.json();
    const session = await getSession({ req });

    if (!session) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    try {
        const newBooking = await prisma.booking.create({
            data: {
                date: new Date(date),
                type,
                userId: session.user.id,
            },
        });
        return NextResponse.json(newBooking, { status: 201 });
    } catch (error) {
        console.error('Error creating booking:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}