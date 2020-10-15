// @flow
/*
  Copyright(c) 2018 Uber Technologies, Inc.
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
          http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

/*
  Example config for GraphView component
*/
import React from "react";

export const NODE_KEY = "id"; // Key used to identify nodes

// These keys are arbitrary (but must match the config)
// However, GraphView renders text differently for empty types
// so this has to be passed in if that behavior is desired.
export const EMPTY_TYPE = "empty";
export const CUSTOM_EMPTY_TYPE = "customEmpty"; // Empty node type
export const POLY_TYPE = "poly";
export const SPECIAL_TYPE = "special";
export const SKINNY_TYPE = "skinny";
export const SPECIAL_CHILD_SUBTYPE = "specialChild";
export const EMPTY_EDGE_TYPE = "emptyEdge";
export const SPECIAL_EDGE_TYPE = "specialEdge";
export const GOLD_NODE = "goldnode";

export const nodeTypes = [
  EMPTY_TYPE,
  CUSTOM_EMPTY_TYPE,
  POLY_TYPE,
  SPECIAL_TYPE,
  SKINNY_TYPE,
  GOLD_NODE
];
export const edgeTypes = [EMPTY_EDGE_TYPE, SPECIAL_EDGE_TYPE];

export const nodeSubTypes = [SPECIAL_CHILD_SUBTYPE];

const Goldnode = (
  <symbol viewBox="0 0 200 200" id="goldnode" width="154" height="154">
    <circle cx="100" cy="100" r="50" fill="rgba(255, 165, 0)"/>
  </symbol>
);

const EmptyNodeShape = (
  <symbol viewBox="0 0 154 154" width="154" height="154" id="emptyNode">
    <circle cx="77" cy="77" r="76" />
  </symbol>
);

const CustomEmptyShape = (
  <symbol viewBox="0 0 200 200" id="customEmpty">
    <circle cx="100" cy="100" r="50" />
    <g>
      <foreignObject width="100%" height="100%">
        <div xmlns="http://www.w3.org/1999/xhtml">test</div>
      </foreignObject>
    </g>
  </symbol>
);

const SpecialShape = (
  <symbol viewBox="-27 0 154 154" id="special" width="154" height="154">
    <rect transform="translate(50) rotate(45)" width="109" height="109" />
  </symbol>
);

const PolyShape = (
  <symbol viewBox="0 0 88 72" id="poly" width="88" height="88">
    <path d="M 0 36 18 0 70 0 88 36 70 72 18 72Z" />
  </symbol>
);

const SkinnyShape = (
  <symbol
    viewBox="0 0 154 54"
    width="154"
    height="54"
    id="skinny"
    onClick={() => console.log("tim")}
  >
    <rect x="0" y="0" rx="2" ry="2" width="154" height="54" />
  </symbol>
);

const SpecialChildShape = (
  <symbol viewBox="0 0 154 154" id="specialChild">
    <rect
      x="2.5"
      y="0"
      width="154"
      height="154"
      fill="rgba(30, 144, 255, 0.12)"
    />
  </symbol>
);

const EmptyEdgeShape = (
  <symbol viewBox="0 0 50 50" id="emptyEdge">
    <circle cx="25" cy="25" r="8" fill="currentColor" />
  </symbol>
);

const SpecialEdgeShape = (
  <symbol viewBox="0 0 50 50" id="specialEdge">
    <rect
      transform="rotate(45)"
      x="27.5"
      y="-7.5"
      width="15"
      height="15"
      fill="currentColor"
    />
  </symbol>
);

export default {
  EdgeTypes: {
    emptyEdge: {
      shape: EmptyEdgeShape,
      shapeId: "#emptyEdge",
      typeText: "Empty"
    },
    specialEdge: {
      shape: SpecialEdgeShape,
      shapeId: "#specialEdge"
    }
  },
  NodeSubtypes: {
    specialChild: {
      shape: SpecialChildShape,
      shapeId: "#specialChild"
    }
  },
  NodeTypes: {
    empty: {
      shape: EmptyNodeShape,
      shapeId: "#empty",
      typeText: "None"
    },
    customEmpty: {
      shape: CustomEmptyShape,
      shapeId: "#customEmpty",
      typeText: "Node"
    },
    special: {
      shape: SpecialShape,
      shapeId: "#special",
      typeText: "Root"
    },
    skinny: {
      shape: SkinnyShape,
      shapeId: "#skinny",
      typeText: "Skinny"
    },
    poly: {
      shape: PolyShape,
      shapeId: "#poly",
      typeText: "Poly"
    },
    goldnode: {
      shape: Goldnode,
      shapeId: "#goldnode",
      typeText: "Gold"
    },
  }
};
