#!/bin/bash
export WONT_FIX=invalid-name,bad-indentation,trailing-newlines,fixme,c-extension-no-member,line-too-long,trailing-whitespace,bad-whitespace
export CATCHALL_MAY_FIX_LATER=no-else-continue,bad-continuation,too-many-arguments,too-many-locals,unused-argument,pointless-string-statement,too-many-instance-attributes,too-few-public-methods,attribute-defined-outside-init,protected-access,unused-variable,too-many-function-args,no-self-use,no-method-argument,function-redefined,too-many-public-methods,anomalous-backslash-in-string,arguments-differ,too-many-boolean-expressions,too-many-statements,no-else-return,too-many-nested-blocks,too-many-lines,too-many-return-statements,eval-used,empty-docstring,unbalanced-tuple-unpacking,global-statement,duplicate-key,redefined-argument-from-local,missing-docstring,unused-wildcard-import,invalid-unary-operand-type,wildcard-import,exec-used,bare-except,duplicate-code,unsubscriptable-object,redefined-outer-name,no-member,too-many-branches
export PYLINT="pylint --disable=$WONT_FIX,$CATCHALL_MAY_FIX_LATER"

find . -iname "*.py" | xargs $PYLINT
