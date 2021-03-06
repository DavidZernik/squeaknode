import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
  Typography,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import BuyOfferItem from "../../components/BuyOfferItem";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";

import {
  getBuyOffersRequest,
} from "../../squeakclient/requests"


export default function BuyPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [offers, setOffers] = useState([]);

  const getOffers = (hash) => {
      getBuyOffersRequest(hash, setOffers);
  };

  const goToOfferPage = (offerId) => {
    console.log("Go to offer page for id: " + offerId);
    history.push("/app/offer/" + offerId);
  };

  useEffect(()=>{
    getOffers(hash)
  },[hash]);

  function OffersContent() {
    return (
      <>
        <Typography variant="h3">
          Offers
        </Typography>
        <div>
          {offers.map(offer =>
            <Box
              p={1}
              key={offer.getOfferId()}
              >
            <BuyOfferItem
              key={offer.getOfferId()}
              handleOfferClick={() => goToOfferPage(offer.getOfferId())}
              offer={offer}>
            </BuyOfferItem>
            </Box>
          )}
        </div>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Buy squeak" />
      {OffersContent()}
    </>
  );
}
