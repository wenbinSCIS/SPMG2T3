"use strict";

// .mjs file (js module), normally using TS

import "dotenv/config";
import Fastify from "fastify";
import cors from "@fastify/cors";
import { PrismaClient } from "@prisma/client";

const port = 5104;
const host = process.env.Host || "127.0.0.1";
const prisma = new PrismaClient();
const fastify = Fastify({ logger: true });

/**
 * 
 * @param {Fastify.FastifyInstance} app 
 * @param {Fastify.FastifyPluginOptions} opts 
 */
async function learningJourney(app, opts) {
  app.get("/getAll", async function(request, reply) {
    const { UserID, Saved } = request.query;
    const savedInt = parseInt(Saved);
    try {
      if (!UserID) throw { status: 400, message: "UserID cannot be null." };
      if (Saved !== 0 && Saved !== 1) throw { status: 400, message: "Saved must be 0 or 1." };
      const data = await prisma.learningJourney.findMany({
        where: { UserID: parseInt(UserID), Saved: savedInt },
        select: { LJID: true }
      });
      return { data };
    } catch (err) {
      return { err }
    }
  });
  app.get("/getById", async function(request, reply) {
    const { LJID } = request.query;
    try {
      if (!LJID) throw { status: 400, message: "LJID cannot be null" };
      const data = await prisma.learningJourney.findUniqueOrThrow({
        where: { LJID: parseInt(LJID) },
        select: { LJID: true }
      });
      return { data };
    } catch (err) {
      return { err }
    }
  });
  app.post("/create", async function(request, reply) {
    const { UserID, Saved } = request.body;
    try {
      if (!UserID) throw { status: 400, message: "UserID cannot be null." };
      if (Saved !== 0 && Saved !== 1) throw { status: 400, message: "Saved must be 0 or 1." };
      const data = await prisma.learningJourney.create({ data: { UserID, Saved } });
      return { data };
    } catch (err) {
      return { err }
    }
  });
}

fastify.register(cors, {});
fastify.register(learningJourney, { prefix: "/LJ" });

(async function() {
  try {
    await fastify.listen({ port, host });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
})();