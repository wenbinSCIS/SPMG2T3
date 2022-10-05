"use strict";

// .mjs file (js module), normally using TS

import "dotenv/config";
import Fastify from "fastify";
import cors from "@fastify/cors";
import { PrismaClient } from "@prisma/client";

const port = 5105;
const host = process.env.Host || "127.0.0.1";
const prisma = new PrismaClient();
const fastify = Fastify({ logger: true });

/**
 * 
 * @param {Fastify.FastifyInstance} app 
 * @param {Fastify.FastifyPluginOptions} opts 
 */
async function learningJourneyCourses(app, opts) {
  app.get("/getAll", async function(request, reply) {
    const { LJID } = request.query;
    try {
      if (!LJID) throw { status: 400, message: "LJID cannot be null" };
      const data = await prisma.learningJourney.findMany({
        where: { LJID: parseInt(LJID) },
        select: { LJCID: true }
      });
      return { status: 200, data };
    } catch (err) {
      return { status: err.status, message: err.message }
    }
  });
  app.get("/getById", async function(request, reply) {
    const { LJCID } = request.query;
    try {
      if (!LJCID) throw { status: 400, message: "LJCID cannot be null" };
      const data = await prisma.learningJourney.findUniqueOrThrow({
        where: { LJCID: parseInt(LJCID) },
        select: { LJCID: true }
      });
      return { status: 200, data };
    } catch (err) {
      return { status: err.status, message: err.message }
    }
  });
  app.post("/create", async function(request, reply) {
    const { LJID, CourseID } = request.body;
    try {
      if (!LJID || !CourseID) throw { status: 400, message: "LJID & CourseID cannot be null" };
      const data = await prisma.learningJourney.create({ data: { LJID, CourseID } });
      return { status: 200, data };
    } catch (err) {
      return { status: err.status, message: err.message }
    }
  });
}

fastify.register(cors, {});
fastify.register(learningJourneyCourses, { prefix: "/LJC" });

(async function() {
  try {
    await fastify.listen({ port, host });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
})();