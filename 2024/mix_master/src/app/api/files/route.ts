import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';
import { getSession } from 'next-auth/react';

const prisma = new PrismaClient();

export async function GET(req: NextApiRequest, res: NextApiResponse) {
    const session = await getSession({ req });

    if (!session) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    try {
        const uploadedFiles = await prisma.file.findMany({
            where: { userId: session.user.id, type: 'uploaded' },
        });

        const receivedFiles = await prisma.file.findMany({
            where: { userId: session.user.id, type: 'received' },
        });

        res.status(200).json({ uploadedFiles, receivedFiles });
    } catch (error) {
        console.error('Error fetching files:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}

export { GET };
