// news-image-20261121 entry point (Node 22, standard library only).
//
// The entry is one image, entry.png, composed by generate.py: a dense front
// page of the world news of Saturday 21 November 2026. This program copies it
// to the grader's output directory. It runs with no arguments and no network.
//
// Outside the grader container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), target);
console.log(`wrote ${target}`);
