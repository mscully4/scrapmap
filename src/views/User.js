import React, { memo } from 'react';
import { useParams } from "react-router-dom";
import { makeStyles } from '@material-ui/styles';

const styles = makeStyles(theme => ({
}))


function User(props) {
  let params = useParams();
  
  const classes = styles();
  return (
  <div style={{"height": window.innerHeight}}>
  </div>
  )
}

export default memo(User)
