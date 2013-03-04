#!/bin/sh

case "$SSH_ORIGINAL_COMMAND" in
*\&*)
echo "Rejected"
;;
*\(*)
echo "Rejected"
;;
*\{*)
echo "Rejected"
;;
*\;*)
echo "Rejected"
;;
*\<*)
echo "Rejected"
;;
*\`*)
echo "Rejected"
;;
*\|*)
echo "Rejected"
;;
rsync\ --server*)
$SSH_ORIGINAL_COMMAND
;;
rsync\ --server*)
$SSH_ORIGINAL_COMMAND
;;
rsync\ --server*/)
$SSH_ORIGINAL_COMMAND
;;
/usr/local/sysadmin/createSnapshotZimbra.sh)
$SSH_ORIGINAL_COMMAND
;;
/usr/local/sysadmin/deleteSnapshotZimbra.sh)
$SSH_ORIGINAL_COMMAND
;;
*)
echo "Rejected"
;;
esac 
