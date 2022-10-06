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
  app.get("/getAll", async (request, reply) => {
    const { UserID, Saved } = request.query;
    const UserID_int = parseInt(UserID);
    const savedInt = parseInt(Saved);
    try {
      if (!UserID || typeof UserID_int !== "number") throw new Error("UserID must be a number and not null");
      if (savedInt !== 0 && savedInt !== 1) throw new Error("Saved must be 0 or 1.");
      const data = await prisma.learningJourney.findMany({
        where: { UserID: UserID_int, Saved: savedInt },
        select: { LJID: true }
      });
      return { data };
    } catch (err) {
      return { err };
    }
  });
  app.get("/getById", async (request, reply) => {
    const { LJID } = request.query;
    const LJID_int = parseInt(LJID);
    try {
      if (!LJID || typeof LJID_int !== "number") throw new Error("LJID must be a number and not null");
      const data = await prisma.learningJourney.findUniqueOrThrow({
        where: { LJID: LJID_int },
        select: { LJID: true }
      });
      return { data };
    } catch (err) {
      return { err };
    }
  });
  app.post("/create", async (request, reply) => {
    const { UserID, Saved } = request.body;
    try {
      if (!UserID || typeof UserID !== "number") throw new Error("UserID must be a number and not null");
      if (Saved !== 0 && Saved !== 1) throw new Error("Saved must be 0 or 1.");
      const data = await prisma.learningJourney.create({ data: { UserID, Saved } });
      return { data };
    } catch (err) {
      return { err };
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