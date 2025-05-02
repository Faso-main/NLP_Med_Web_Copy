import React from "react";

import "css/Line.css"

const Line = ({ isBoldName, name, value }) => {
  return (
        <div className={`line ${isBoldName ? 'isbold' : ''}`}>
            <p className="name">{name}:</p>
            <p className="value">{value}</p>
        </div>
  );
};

export default Line;
