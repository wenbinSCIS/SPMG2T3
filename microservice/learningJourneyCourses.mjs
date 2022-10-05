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
async function learningJourneyCourses(app, opts) {
  app.get("/getAll", async function(request, reply) {
    const { LJID } = request.query;
    try {
      if (!LJID) throw { statusCode: 400, message: "LJID cannot be null" };
      const data = await prisma.learningJourney.findMany({
        where: { LJID: parseInt(LJID) },
        select: { LJCID: true }
      });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
  app.get("/getById", async function(request, reply) {
    const { LJCID } = request.query;
    try {
      if (!LJCID) throw { statusCode: 400, message: "LJCID cannot be null" };
      const data = await prisma.learningJourney.findUniqueOrThrow({
        where: { LJCID: parseInt(LJCID) },
        select: { LJCID: true }
      });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
  app.post("/create", async function(request, reply) {
    const { LJID, CourseID } = request.body;
    try {
      if (!LJID || !CourseID) throw { statusCode: 400, message: "LJID & CourseID cannot be null" };
      const data = await prisma.learningJourney.create({ data: { LJID, CourseID } });
      return { statusCode: 200, data };
    } catch (err) {
      return { statusCode: err.status, message: err.message }
    }
  });
}

fastify.register(learningJourneyCourses, { prefix: "/LJC" });

(async function() {
  try {
    await fastify.listen({ port, host });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
})();