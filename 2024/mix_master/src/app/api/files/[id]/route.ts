import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function GET(req: NextApiRequest, res: NextApiResponse) {
    const { id } = req.query;

    try {
        const file = await prisma.file.findUnique({
            where: { id: Number(id) },
        });

        if (!file) {
            return res.status(404).json({ error: 'File not found' });
        }

        res.status(200).json(file);
    } catch (error) {
        console.error('Error fetching file:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}

export { GET };
