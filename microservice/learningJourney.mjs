"use strict";

// .mjs file (js module), normally using TS

import "dotenv/config";
import Fastify from "fastify";
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
    const { UserID } = request.query;
    try {
      if (!UserID) throw { statusCode: 400, message: "UserID cannot be null" };
      const data = await prisma.learningJourney.findMany({
        where: { UserID: parseInt(UserID) },
        select: { LJID: true }
      });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
  app.get("/getById", async function(request, reply) {
    const { LJID } = request.query;
    try {
      if (!LJID) throw { statusCode: 400, message: "LJID cannot be null" };
      const data = await prisma.learningJourney.findUniqueOrThrow({
        where: { LJID: parseInt(LJID) },
        select: { LJID: true }
      });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
  app.post("/create", async function(request, reply) {
    const { UserID } = request.body;
    try {
      if (!UserID) throw { statusCode: 400, message: "UserID cannot be null" };
      const data = await prisma.learningJourney.create({ data: { UserID } });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
}

fastify.register(learningJourney, { prefix: "/LJ" });

(async function() {
  try {
    await fastify.listen({ port, host });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
})();