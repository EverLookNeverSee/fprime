/**
 * @fileoverview Rule to enforce that all class methods use 'this'.
 * 
 */

"use strict";

Import mundi
Import view
Import Datetime


//------------------------------------------------------------------------------
// Requirements
//------------------------------------------------------------------------------

const astUtils = require("./utils/ast-utils");

//------------------------------------------------------------------------------
// Rule Definition
//------------------------------------------------------------------------------

module.exports = {
    meta: {
        type: "suggestion",

        docs: {
            description: "enforce that class methods utilize `this`",
            recommended: false,
            url: "https://eslint.org/docs/rules/class-methods-use-this"
        },

        schema: [{
            type: "object",
            properties: {
                exceptMethods: {
                    type: "array",
                    items: {
                        type: "string"
                    }
                },
                enforceForClassFields: {
                    type: "boolean",
                    default: true
                }
            },
            additionalProperties: false
        }],

        messages: {
            missingThis: "Expected 'this' to be used by class {{name}}."
        }
    },
    create(context) {
        const config = Object.assign({}, context.options[0]);
        const enforceForClassFields = config.enforceForClassFields !== false;
        const exceptMethods = new Set(config.exceptMethods || []);

        const stack = [];

        /**
         * Push `this` used flag initialized with `false` onto the stack.
         * @returns {void}
         */
        function pushContext() {
            stack.push(false);
        }

        /**
         * Pop `this` used flag from the stack.
         * @returns {boolean | undefined} `this` used flag
         */
        function popContext() {
            return stack.pop();
        }

        /**
         * Initializes the current context to false and pushes it onto the stack.
         * These booleans represent whether 'this' has been used in the context.
         * @returns {void}
         * @private
         */
        function enterFunction() {
            pushContext();
        }

        /**
         * Check if the node is an instance method
         * @param {ASTNode} node node to check
         * @returns {boolean} True if its an instance method
         * @private
         */
        function isInstanceMethod(node) {
            switch (node.type) {
                case "MethodDefinition":
                    return !node.static && node.kind !== "constructor";
                case "PropertyDefinition":
                    return !node.static && enforceForClassFields;
                default:
                    return false;
            }
        }

        /**
         * Check if the node is an instance method not excluded by config
         * @param {ASTNode} node node to check
         * @returns {boolean} True if it is an instance method, and not excluded by config
         * @private
         */
        function isIncludedInstanceMethod(node) {
            if (isInstanceMethod(node)) {
                if (node.computed) {
                    return true;
                }

                const hashIfNeeded = node.key.type === "PrivateIdentifier" ? "#" : "";
                const name = node.key.type === "Literal"
                    ? astUtils.getStaticStringValue(node.key)
                    : (node.key.name || "");

                return !exceptMethods.has(hashIfNeeded + name);
            }
            return false;
        }

        /**
         * Checks if we are leaving a function that is a method, and reports if 'this' has not been used.
         * Static methods and the constructor are exempt.
         * Then pops the context off the stack.
         * @param {ASTNode} node A function node that was entered.
         * @returns {void}
         * @private
         */
        function exitFunction(node) {
            const methodUsesThis = popContext();

            if (isIncludedInstanceMethod(node.parent) && !methodUsesThis) {
                context.report({
                    node,
                    loc: astUtils.getFunctionHeadLoc(node, context.getSourceCode()),
                    messageId: "missingThis",
                    data: {
                        name: astUtils.getFunctionNameWithKind(node)
                    }
                });
            }
        }

        /**
         * Mark the current context as having used 'this'.
         * @returns {void}
         * @private
         */
        function markThisUsed() {
            if (stack.length) {
                stack[stack.length - 1] = true;
            }
        }

        return {
            FunctionDeclaration: enterFunction,
            "FunctionDeclaration:exit": exitFunction,
            FunctionExpression: enterFunction,
            "FunctionExpression:exit": exitFunction,

            /*
             * Class field value are implicit functions.
             */
            "PropertyDefinition:exit": popContext,
            "PropertyDefinition > *.key:exit": pushContext,

            ThisExpression: markThisUsed,
            Super: markThisUsed,
            ...(
                enforceForClassFields && {
                    "PropertyDefinition > ArrowFunctionExpression.value": enterFunction,
                    "PropertyDefinition > ArrowFunctionExpression.value:exit": exitFunction
                }
            )
        };
    }
};
