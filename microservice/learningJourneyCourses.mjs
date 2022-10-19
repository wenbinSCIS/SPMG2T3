"use strict";

// .mjs file (js module), normally using TS

import "dotenv/config";
import Fastify from "fastify";
import cors from "@fastify/cors";
import fetch from "node-fetch"; // standby import, in case someone not using Node.js 18
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
  app.get("/getAll", async (request, reply) => {
    const { LJID } = request.query;
    const LJID_int = parseInt(LJID)
    try {
      if (!LJID || typeof LJID_int !== "number") throw new Error("LJID must be a number and not null");
      const data = await prisma.learningJourneyCourses.findMany({
        where: { LJID: LJID_int },
        select: { LJCID: true, CourseID: true },
      });
      const courses = [];
      for (let { LJCID, CourseID } of data) {
        const res = await fetch(`http://127.0.0.1:5004/getCoursebyId?cid=${CourseID}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        const { data } = await res.json();
        courses.push({ LJCID, ...data[0] });
      }
      return { data: courses };
    } catch (err) {
      return { err }
    }
  });
  app.get("/getById", async (request, reply) => {
    const { LJCID } = request.query;
    const LJCID_int = parseInt(LJCID);
    try {
      if (!LJCID || typeof LJCID_int !== "number") throw new Error("LJCID must be a number and not null");
      const data = await prisma.learningJourneyCourses.findUniqueOrThrow({
        where: { LJCID: LJCID_int },
        select: { LJCID: true }
      });
      return { data };
    } catch (err) {
      return { err }
    }
  });
  app.post("/create", async (request, reply) => {
    const { LJID, CourseID } = request.body;
    try {
      if (!LJID || typeof LJID !== "number") throw new Error("LJID must be a number and not null.");
      if (!CourseID || typeof CourseID !== "string") throw new Error("CourseID must not be an empty string and not null.");
      const data = await prisma.learningJourneyCourses.create({ data: { LJID, CourseID } });
      return { data };
    } catch (err) {
      return { err }
    }
  });
  // update not needed since that isn't how it works, how it works is just create and delete, each LJC is LJ + 1 course
  // so to update the course, we create a new row, where LJ is the same, but course is different (the idea is dropping courses should drop the row)
  app.delete("/delete", async (request, response) => {
    const { LJCID } = request.body;
    try {
      if (!LJCID) throw new Error("LJCID must be a number and not null");
      const data = await prisma.learningJourneyCourses.delete({
        where: { LJCID },
      });
      return { data };
    } catch (err) {
      return { err };
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